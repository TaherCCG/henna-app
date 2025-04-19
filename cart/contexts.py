from django.conf import settings
from django.shortcuts import get_object_or_404
from decimal import Decimal, ROUND_HALF_UP
from products.models import HennaProduct

def cart_contents(request):
    """Retrieve the contents of the cart and calculate totals without VAT and delivery by default."""

    cart_items = []
    total = Decimal('0.00')
    product_count = 0
    cart = request.session.get('cart', {})

    for item_id, item_data in cart.items():
        quantity = int(item_data.get('quantity', 1))
        product = get_object_or_404(HennaProduct, pk=item_id)
        
        discounted_price = Decimal(item_data.get('discounted_price', '0.00'))
        
        total += quantity * discounted_price
        product_count += quantity
        
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
            'discounted_price': discounted_price,
        })

    # Round total to 2 decimal places
    total = total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    grand_total = total

    # Add VAT and delivery cost on cart or checkout pages
    if request.path in ['/cart/', '/checkout/']:
        vat_rate = Decimal('0.20')  # 20% VAT
        vat_amount = (total * vat_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        if total >= settings.FREE_DELIVERY_THRESHOLD:
            delivery_cost = Decimal('0.00')
        else:
            delivery_cost = Decimal('4.99').quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        grand_total += vat_amount + delivery_cost
    else:
        vat_amount = Decimal('0.00')
        delivery_cost = Decimal('0.00')

    free_delivery_threshold = Decimal(settings.FREE_DELIVERY_THRESHOLD)
    free_delivery_delta = free_delivery_threshold - total if total < free_delivery_threshold else Decimal('0.00')

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'grand_total': grand_total,
        'vat_amount': vat_amount,
        'delivery_cost': delivery_cost,
        'free_delivery_threshold': free_delivery_threshold,
        'free_delivery_delta': free_delivery_delta,
    }

    return context