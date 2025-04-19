from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from .models import Delivery

def calculate_delivery_cost_and_totals(cart_total):
    """
    Calculate delivery cost, VAT, and grand total based on the cart total.
    """
    free_delivery_threshold = Decimal(settings.FREE_DELIVERY_THRESHOLD)
    vat_rate = Decimal(settings.VAT_RATE)
    
    # Fetch delivery methods
    delivery_methods = Delivery.objects.filter(active=True)
    
    # Default values
    delivery_cost = Decimal('0.00')
    delivery_name = 'Standard Delivery'
    
    # Determine delivery cost
    if cart_total < free_delivery_threshold:
        standard_delivery = delivery_methods.filter(name='Standard Delivery').first()
        if standard_delivery:
            delivery_cost = standard_delivery.cost
            delivery_name = standard_delivery.name
    else:
        free_delivery = delivery_methods.filter(name='Free Delivery').first()
        if free_delivery:
            delivery_cost = Decimal('0.00')
            delivery_name = free_delivery.name

    # Calculate free delivery delta
    free_delivery_delta = free_delivery_threshold - cart_total if cart_total < free_delivery_threshold else Decimal('0.00')
    
    # VAT calculation
    vat_amount = (cart_total * vat_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    # Grand total (cart + vat)
    grand_total = (cart_total + vat_amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    # Grand total + Delivery
    grand_total_with_vat = (grand_total + delivery_cost).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    return {
        'delivery_cost': delivery_cost,
        'delivery_name': delivery_name,
        'vat_amount': vat_amount,
        'grand_total': grand_total,
        'grand_total_with_vat': grand_total_with_vat,
        'free_delivery_delta': free_delivery_delta,
    }
