from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.utils import timezone
from django.http import HttpResponse
from django.urls import reverse 
from .models import HennaProduct, ProductsCategory, Discount
from .forms import ProductForm, DiscountForm

def all_products(request):
    """A view to show all products, including sorting and search queries."""

    products = HennaProduct.objects.all()
    query = None
    categories = None
    sort = None
    direction = None
    discounted = request.GET.get('discounted') == 'true'

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__friendly_name__in=categories)
            categories = ProductsCategory.objects.filter(friendly_name__in=categories).order_by('friendly_name')

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

        if discounted:
            products = products.filter(
                discounts__active=True,
                discounts__start_date__lte=timezone.now(),
                discounts__end_date__gte=timezone.now()
            ).distinct()

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """A view to show individual product details, including discounted price and discount name."""

    product = get_object_or_404(HennaProduct, pk=product_id)
    discounted_price = product.get_discounted_price()

    discount_name = None
    current_discount = product.get_current_discount()
    if current_discount:
        discount_name = current_discount.name

    context = {
        'product': product,
        'discounted_price': discounted_price,
        'discount_name': discount_name,
    }

    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """A view to add a new product."""

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('products')
    else:
        form = ProductForm()
    
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Add Product'})


def edit_product(request, product_id):
    """A view to edit an existing product."""

    product = get_object_or_404(HennaProduct, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Edit Product'})


def delete_product(request, product_id):
    """A view to delete a product."""
    
    product = get_object_or_404(HennaProduct, pk=product_id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('products')

    return HttpResponse(status=405)


def add_discount(request):
    """A view to add a new discount."""

    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Discount added successfully!')
            return redirect('products')
    else:
        form = DiscountForm()
    
    return render(request, 'products/discount_form.html', {'form': form, 'title': 'Add Discount'})


def edit_discount(request, discount_id):
    """A view to edit an existing discount."""

    discount = get_object_or_404(Discount, pk=discount_id)

    if request.method == 'POST':
        form = DiscountForm(request.POST, instance=discount)
        if form.is_valid():
            form.save()
            messages.success(request, 'Discount updated successfully!')
            return redirect('products')
    else:
        form = DiscountForm(instance=discount)

    return render(request, 'products/discount_form.html', {'form': form, 'title': 'Edit Discount'})


def delete_discount(request, discount_id):
    """A view to delete a discount."""
    
    discount = get_object_or_404(Discount, pk=discount_id)

    if request.method == 'POST':
        discount.delete()
        messages.success(request, 'Discount deleted successfully!')
        return redirect('products')

    return HttpResponse(status=405) 
