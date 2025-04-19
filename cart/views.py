from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from decimal import Decimal
from products.models import HennaProduct
from django.http import JsonResponse
from django.conf import settings
from checkout.utils import calculate_delivery_cost_and_totals

def view_cart(request):
    """Retrieve and display the shopping cart contents and calculate totals."""
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0.00')

    for item_id, item_data in cart.items():
        quantity = item_data.get('quantity', 1)
        discounted_price = Decimal(item_data.get('discounted_price', '0.00'))
        product = get_object_or_404(HennaProduct, id=item_id)
        subtotal = quantity * discounted_price

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'discounted_price': discounted_price,
            'subtotal': subtotal
        })
        total += subtotal

    totals = calculate_delivery_cost_and_totals(total)

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'delivery': totals['delivery_cost'],
        'vat_amount': totals['vat_amount'],
        'grand_total': totals['grand_total_with_vat'],
        'free_delivery_delta': totals['free_delivery_delta']
    })

def add_to_cart(request, item_id):
    """Add a specified quantity of a product to the shopping cart with its discounted price."""
    product = get_object_or_404(HennaProduct, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url', '/')

    cart = request.session.setdefault('cart', {})
    discounted_price = product.get_discounted_price()
    str_item_id = str(item_id)

    if str_item_id in cart:
        cart[str_item_id]['quantity'] += quantity
        messages.success(request, f'Updated {product.name} quantity to {cart[str_item_id]["quantity"]}')
    else:
        cart[str_item_id] = {
            'quantity': quantity,
            'discounted_price': str(discounted_price)
        }
        messages.success(request, f'Added {product.name} to your shopping cart.')

    request.session.modified = True
    return redirect(redirect_url)

def adjust_cart(request, item_id):
    """Adjust the quantity of a specific product in the cart."""
    if request.method != 'POST':
        return redirect('view_cart')

    product = get_object_or_404(HennaProduct, pk=item_id)
    quantity = int(request.POST.get('quantity', 0))
    str_item_id = str(item_id)
    cart = request.session.get('cart', {})

    if str_item_id in cart:
        if quantity > 0:
            cart[str_item_id]['quantity'] = quantity
            messages.success(request, f'Updated {product.name} quantity to {quantity}')
        else:
            cart.pop(str_item_id)
            messages.warning(request, f'Removed {product.name} from your shopping cart.')
    else:
        messages.error(request, f'{product.name} was not found in your cart.')

    request.session['cart'] = cart
    return redirect('view_cart')

def remove_from_cart(request, item_id):
    """Remove a product from the shopping cart."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    product = get_object_or_404(HennaProduct, pk=item_id)
    str_item_id = str(item_id)
    cart = request.session.get('cart', {})

    if str_item_id in cart:
        cart.pop(str_item_id)
        messages.success(request, f'Removed {product.name} from your shopping cart.')
        request.session['cart'] = cart
        return JsonResponse({'success': True, 'message': f'Removed {product.name} from your cart.'})
    else:
        messages.error(request, f'{product.name} was not found in your cart.')
        return JsonResponse({'error': 'Item not found in cart'}, status=404)
