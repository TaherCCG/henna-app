from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from decimal import Decimal, ROUND_HALF_UP
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required, user_passes_test

from profiles.forms import UserProfileForm
from .forms import OrderForm, DeliveryForm
from .models import Delivery, Order, OrderItem, HennaProduct, UserProfile 
from cart.contexts import cart_contents
from .utils import calculate_delivery_cost_and_totals

import stripe
import json

from .webhook_handler import StripeWH_Handler 

stripe_public_key = settings.STRIPE_PUBLIC_KEY
stripe_secret_key = settings.STRIPE_SECRET_KEY


def create_new_payment_intent(amount):
    """
    Helper function to create a new PaymentIntent with standard settings.
    Preserves Stripe's automatic payment methods feature.
    """
    return stripe.PaymentIntent.create(
        amount=amount,
        currency=settings.STRIPE_CURRENCY,
        automatic_payment_methods={'enabled': True},
        metadata={'initiated_from': 'checkout_page'}
    )


@require_POST
def cache_checkout_data(request):
    """
    Cache checkout data on the PaymentIntent before payment is processed.
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = stripe_secret_key
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user.username if request.user.is_authenticated else '',
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request,
            'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=str(e), status=400)


def checkout(request):
    """
    Display checkout form and handle payment processing.
    Reuses existing PaymentIntents or creates new ones.
    """
    current_cart = cart_contents(request)
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    # Calculate costs
    delivery_cost = current_cart.get('delivery_cost', Decimal('0.00'))
    calculations = calculate_delivery_cost_and_totals(current_cart['total'], delivery_cost)

    # Stripe setup
    stripe.api_key = stripe_secret_key
    stripe_total = int((calculations['grand_total_with_vat'] * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

        # ----- Handle POST (form submission) -----
    if request.method == 'POST':
        payment_intent_id = request.POST.get('payment_intent_id')

        # Handle order form submission
        form_data = {
            'full_name':        request.POST['full_name'],
            'email':            request.POST['email'],
            'phone_number':     request.POST['phone_number'],
            'country':          request.POST['country'],
            'postcode':         request.POST['postcode'],
            'town_or_city':     request.POST['town_or_city'],
            'street_address1':  request.POST['street_address1'],
            'street_address2':  request.POST.get('street_address2', ''),
            'county':           request.POST.get('county', ''),
        }
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)

            # Get and assign delivery method safely
            delivery_method_id = request.POST.get('delivery_method')
            selected_delivery = None
            if delivery_method_id:
                try:
                    selected_delivery = Delivery.objects.get(id=delivery_method_id)
                except Delivery.DoesNotExist:
                    messages.error(request, "Selected delivery method not found.")
                    return redirect('checkout')

            order.delivery_method = selected_delivery
            order.save()

            # Get the updated delivery cost based on the selected method
            delivery_cost = selected_delivery.cost  

            # Recalculate the totals with the updated delivery cost
            calculations = calculate_delivery_cost_and_totals(current_cart['total'], delivery_cost)

            # Update Stripe total with the new grand total (including updated delivery cost)
            stripe_total = int((calculations['grand_total_with_vat'] * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

            try:
                # Try retrieving and updating existing PaymentIntent
                intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                if intent.amount != stripe_total:
                    stripe.PaymentIntent.modify(
                        payment_intent_id,
                        amount=stripe_total,
                        metadata={
                            'cart': json.dumps(cart),
                            'save_info': request.POST.get('save_info'),
                            'username': request.user.username if request.user.is_authenticated else '',
                            'delivery_method_id': str(selected_delivery.id)
                        }
                    )
                client_secret = intent.client_secret
                request.session['payment_intent_id'] = intent.id

            except stripe.error.StripeError:
                # Create new PaymentIntent if there's an issue
                intent = create_new_payment_intent(stripe_total)
                client_secret = intent.client_secret
                request.session['payment_intent_id'] = intent.id

            # Save user profile if requested
            if request.POST.get('save_info') and request.user.is_authenticated:
                profile = UserProfile.objects.get(user=request.user)
                profile.default_phone_number = request.POST.get('phone_number', profile.default_phone_number)
                profile.default_country = request.POST.get('country', profile.default_country)
                profile.default_postcode = request.POST.get('postcode', profile.default_postcode)
                profile.default_town_or_city = request.POST.get('town_or_city', profile.default_town_or_city)
                profile.default_street_address1 = request.POST.get('street_address1', profile.default_street_address1)
                profile.default_street_address2 = request.POST.get('street_address2', profile.default_street_address2)
                profile.default_county = request.POST.get('county', profile.default_county)
                profile.save()

            # Create order line items
            for item in current_cart['cart_items']:
                try:
                    product = HennaProduct.objects.get(id=item['product'].id)
                    order_item = OrderItem(
                        order=order,
                        product=product,
                        quantity=item['quantity'],
                    )
                    order_item.save()
                except HennaProduct.DoesNotExist:
                    messages.error(request, "One of the items in your cart wasn't found in our database.")
                    order.delete()
                    return redirect('view_cart')

            # Finalise order total
            order.update_total()

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))

        else:
            messages.error(request, "There was an issue with your order form. Please check your details and try again.")

    # ----- Handle GET (initial page load) -----
    else:
        if 'payment_intent_id' in request.session:
            try:
                intent = stripe.PaymentIntent.retrieve(request.session['payment_intent_id'])

                # Only reuse if the status is "requires_payment_method" and the amount matches
                if intent.status != 'requires_payment_method' or abs(intent.amount - stripe_total) > stripe_total * 0.05:
                    intent = create_new_payment_intent(stripe_total)

            except stripe.error.StripeError:
                intent = create_new_payment_intent(stripe_total)
        else:
            intent = create_new_payment_intent(stripe_total)

        request.session['payment_intent_id'] = intent.id
        client_secret = intent.client_secret

        # Pre-fill form for logged in users
        order_form_data = {}
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form_data = {
                    'full_name':        request.user.get_full_name(),
                    'email':            request.user.email,
                    'phone_number':     profile.default_phone_number,
                    'country':          profile.default_country,
                    'postcode':         profile.default_postcode,
                    'town_or_city':     profile.default_town_or_city,
                    'street_address1':  profile.default_street_address1,
                    'street_address2':  profile.default_street_address2,
                    'county':           profile.default_county,
                }
            except UserProfile.DoesNotExist:
                pass

        order_form = OrderForm(initial=order_form_data)

    if not stripe_public_key:
        messages.warning(request, "Stripe public key is missing.")

    context = {
        'order_form':               order_form,
        'total_cost':               current_cart['total'],
        'delivery_cost':            calculations['delivery_cost'],
        'grand_total':              calculations['grand_total'],
        'grand_total_with_vat':     calculations['grand_total_with_vat'],
        'vat_amount':               calculations['vat_amount'],
        'delivery_name':            calculations['delivery_name'],
        'free_delivery_threshold':  settings.FREE_DELIVERY_THRESHOLD,
        'is_threshold_met':         current_cart['total'] >= settings.FREE_DELIVERY_THRESHOLD,
        'delivery_methods':         Delivery.objects.filter(active=True),
        'free_delivery_delta':      calculations['free_delivery_delta'],
        'cart_items':               current_cart['cart_items'],
        'product_count':            current_cart['product_count'],
        'stripe_public_key':        stripe_public_key,
        'client_secret':            intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """
    Display order confirmation and send confirmation email.
    """
    save_info = request.session.get('save-info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()
        if save_info:
            profile.default_phone_number      = order.phone_number
            profile.default_country           = order.country
            profile.default_postcode          = order.postcode
            profile.default_town_or_city      = order.town_or_city
            profile.default_street_address1   = order.street_address1
            profile.default_street_address2   = order.street_address2
            profile.default_county            = order.county
            profile.save()
    
    # Update order total
    order.update_total()

    subject       = f'Order Confirmation: {order_number}'
    html_message  = render_to_string('checkout/order_confirmation_email.html', {'order': order})
    plain_message = strip_tags(html_message)
    from_email    = settings.DEFAULT_FROM_EMAIL
    to_email      = order.email

    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

    messages.success(request,
        f'Order successfully processed! Your order number is {order_number}. '
        'A confirmation email has been sent to your email address.')

    # Enhanced cleanup
    if 'cart' in request.session:
        del request.session['cart']
        
    if 'payment_intent_id' in request.session:
        try:
            # Cancel the PaymentIntent to prevent further charges
            stripe.PaymentIntent.cancel(request.session['payment_intent_id'])
        except stripe.error.StripeError as e:
            print(f"Error canceling PaymentIntent: {e}")
            # If already succeeded/canceled, ignore
        finally:
            del request.session['payment_intent_id']

    return render(request, 'checkout/checkout_success.html', {'order': order})


# ----------------------------------------
# Stripe Webhook Endpoint
# ----------------------------------------
@csrf_exempt
def stripe_webhook(request):
    """Stripe webhook endpoint."""
    payload    = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    wh_secret  = settings.STRIPE_WH_SECRET
    print("Webhook Secret (from settings):", wh_secret)
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    handler = StripeWH_Handler(request)

    event_map = {
        'checkout.session.completed':    handler.handle_checkout_session_completed,
        'payment_intent.succeeded':      handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    event_type    = event['type']
    event_handler = event_map.get(event_type, handler.handle_event)

    return event_handler(event)


def calculate_delivery_cost_and_totals(subtotal, delivery_cost):
    """
    Calculate VAT, delivery, and total amounts for the cart.
    Returns a dict with VAT, totals, delivery info, and free delivery delta.
    """
    vat_rate = Decimal('0.20')
    vat_amount = (subtotal * vat_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    grand_total = subtotal + delivery_cost
    grand_total_with_vat = grand_total + vat_amount

    free_delivery_threshold = Decimal(settings.FREE_DELIVERY_THRESHOLD)
    free_delivery_delta = (
        free_delivery_threshold - subtotal if subtotal < free_delivery_threshold else Decimal('0.00')
    )

    return {
        'vat_amount': vat_amount,
        'grand_total': grand_total,
        'grand_total_with_vat': grand_total_with_vat,
        'delivery_cost': delivery_cost,  
        'free_delivery_delta': free_delivery_delta,
        'delivery_name': 'Standard Delivery' if delivery_cost > 0 else 'Free Delivery',  
    }


@require_POST
def update_delivery(request, delivery_id):
    """
    AJAX endpoint to recalc delivery and totals when a delivery method is selected.
    """
    cart = request.session.get('cart', {})
    current_cart = cart_contents(request)
    subtotal = current_cart['total']

    try:
        selected_delivery = Delivery.objects.get(id=delivery_id)
        delivery_cost = selected_delivery.cost
        calculations = calculate_delivery_cost_and_totals(subtotal, delivery_cost)
        
        # Update Stripe PaymentIntent
        stripe_total = int((calculations['grand_total_with_vat'] * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
        
        if 'payment_intent_id' in request.session:
            try:
                intent = stripe.PaymentIntent.modify(
                    request.session['payment_intent_id'],
                    amount=stripe_total,
                    metadata={
                        'cart': json.dumps(cart),
                        'delivery_method_id': str(delivery_id),
                    }
                )
                client_secret = intent.client_secret
            except stripe.error.StripeError:
                # Fallback to creating new intent if modification fails
                intent = create_new_payment_intent(stripe_total)
                request.session['payment_intent_id'] = intent.id
                client_secret = intent.client_secret
        else:
            intent = create_new_payment_intent(stripe_total)
            request.session['payment_intent_id'] = intent.id
            client_secret = intent.client_secret

        return JsonResponse({
            'delivery_cost': float(delivery_cost),
            'grand_total': float(calculations['grand_total']),
            'grand_total_with_vat': float(calculations['grand_total_with_vat']),
            'estimated_delivery_time': selected_delivery.estimated_delivery_time,
            'company_name': selected_delivery.company_name,
            'delivery_name': selected_delivery.name,
            'vat_amount': float(calculations['vat_amount']),
            'client_secret': client_secret, 
        })

    except Delivery.DoesNotExist:
        return JsonResponse({
            'error': 'Selected delivery option is invalid.',
        }, status=400)


# Helper function to check if the user is a superuser
def superuser_required(user):
    return user.is_superuser


@login_required
def add_delivery(request):
    """
    Add a new delivery method through the delivery form.
    Handles form submission for adding delivery methods.
    """
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Delivery method added successfully!")
            return redirect('list_deliveries')
    else:
        form = DeliveryForm()

    context = {
        'form': form,
        'title': 'Add Delivery Method',
        'edit_mode': False,
    }
    return render(request, 'checkout/delivery_form.html', context)


@login_required
def edit_delivery(request, delivery_id):
    """
    Handles form submission for updating delivery methods.
    """
    delivery = get_object_or_404(Delivery, id=delivery_id)
    if request.method == 'POST':
        form = DeliveryForm(request.POST, instance=delivery)
        if form.is_valid():
            form.save()
            messages.success(request, "Delivery method updated successfully!")
            return redirect('list_deliveries')
    else:
        form = DeliveryForm(instance=delivery)

    context = {
        'form': form,
        'title': 'Edit Delivery Method',
        'edit_mode': True,
        'delivery': delivery,
    }
    return render(request, 'checkout/delivery_form.html', context)


@login_required
@require_POST
def delete_delivery(request, delivery_id):
    """
    Handles form submission for deleting delivery methods.
    """
    delivery = get_object_or_404(Delivery, id=delivery_id)

    if request.method == 'POST':
        delivery.delete()
        messages.success(request, "Delivery method deleted successfully!")
        return redirect('list_deliveries')

    return HttpResponse(status=405)


@login_required
@user_passes_test(superuser_required)
def list_deliveries(request):
    """
    List all available delivery methods.
    """
    deliveries = Delivery.objects.all()
    context = {
        'deliveries': deliveries,
    }
    return render(request, 'checkout/list_deliveries.html', context)
