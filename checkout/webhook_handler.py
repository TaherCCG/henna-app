from django.http import HttpResponse
from .models import Order, OrderItem, Delivery
from products.models import HennaProduct
from .utils import calculate_delivery_cost_and_totals
import json
import time
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Generic handler for unexpected webhook events."""
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_checkout_session_completed(self, event):
        """Handle the checkout.session.completed webhook from Stripe"""
        session = event['data']['object']
        # Pull the PaymentIntent ID off the session
        pid = session.get('payment_intent')
        metadata = session.get('metadata', {})

         # Get delivery method from metadata
        delivery_method_id = metadata.get('delivery_method_id')
        if delivery_method_id:
            try:
                delivery_method = Delivery.objects.get(id=delivery_method_id)
                delivery_cost = delivery_method.cost
            except Delivery.DoesNotExist:
                delivery_cost = Decimal('0.00')
        else:
            delivery_cost = Decimal('0.00')
        
        cart = metadata.get('cart')
        save_info = metadata.get('save_info', False)

        if not cart or not pid:
            logger.error('Missing cart or payment intent in session metadata')
            return HttpResponse(status=400)

        # Retrieve the PaymentIntent to get billing/shipping details & amount
        import stripe
        from django.conf import settings
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.retrieve(pid)

        billing_details = intent.charges.data[0].billing_details
        shipping_details = session.get('shipping', {})
        grand_total_with_vat = round(intent.charges.data[0].amount / 100, 2)

        # Clean up any empty shipping address fields
        if 'address' in shipping_details:
            for field, value in shipping_details['address'].items():
                if value == "":
                    shipping_details['address'][field] = None

        # Compute delivery cost & totals
        delivery_cost = self.get_delivery_cost(delivery_method_id)
        totals = calculate_delivery_cost_and_totals(Decimal(grand_total_with_vat))
        
        # Check for an existing order
        if self.check_order_exists(shipping_details, billing_details, cart, pid, grand_total_with_vat):
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200
            )

        # Create the order
        order = self.create_order(
            shipping_details, billing_details, cart, pid,
            delivery_cost,
            totals  # pass the totals dict so create_order can set them
        )
        if not order:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: Order creation failed',
                status=500
            )

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """PaymentIntent succeeded (fallback)"""
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | Ignored (checkout.session.completed preferred)',
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """PaymentIntent failed"""
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )

    def get_delivery_cost(self, delivery_method_id):
        """Retrieve delivery cost based on delivery method ID"""
        if not delivery_method_id:
            logger.error('No delivery method ID provided')
            return Decimal('0.00')
        try:
            delivery_method = Delivery.objects.get(id=delivery_method_id)
            return Decimal(delivery_method.cost)
        except Delivery.DoesNotExist:
            logger.error(f'Delivery method not found: {delivery_method_id}')
            return Decimal('0.00')

    def check_order_exists(self, shipping_details, billing_details, cart, pid, grand_total):
        """Check if an order already exists in the database"""
        address = shipping_details.get('address', {})
        attempt = 1
        while attempt <= 5:
            try:
                Order.objects.get(
                    full_name__iexact=shipping_details.get('name'),
                    email__iexact=billing_details.get('email'),
                    phone_number__iexact=shipping_details.get('phone'),
                    country__iexact=address.get('country'),
                    postcode__iexact=address.get('postal_code'),
                    town_or_city__iexact=address.get('city'),
                    street_address1__iexact=address.get('line1'),
                    street_address2__iexact=address.get('line2'),
                    county__iexact=address.get('state'),
                    grand_total=grand_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                return True
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        return False

    def create_order(self, shipping_details, billing_details, cart, pid, delivery_cost, totals):
        """Create a new order in the database using the passed totals dict."""
        address = shipping_details.get('address', {})
        try:
            order = Order.objects.create(
                full_name=shipping_details.get('name'),
                email=billing_details.get('email'),
                phone_number=shipping_details.get('phone'),
                street_address1=address.get('line1'),
                street_address2=address.get('line2'),
                town_or_city=address.get('city'),
                postcode=address.get('postal_code'),
                county=address.get('state'),
                country=address.get('country'),
                original_cart=cart,
                stripe_pid=pid,
                delivery_cost=totals['delivery_cost'],
                vat_amount=totals['vat_amount'],
                grand_total=totals['grand_total'],
                grand_total_with_vat=totals['grand_total_with_vat'],
            )

            for item_id, item_data in json.loads(cart).items():
                product = HennaProduct.objects.get(id=item_id)
                quantity = item_data if isinstance(item_data, int) else item_data.get('quantity', 1)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                )
            return order
        except Exception as e:
            logger.error(f'Error creating order: {e}')
            return None
