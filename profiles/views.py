from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order

@login_required
def profile(request):
    """ Display and update user profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    # Retrieve the user's order history through the profile
    orders = Order.objects.filter(user_profile=profile)

    template = 'profiles/profile.html'
    context = {
        'profile_form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)


@login_required
def order_history(request, order_number):
    """ A view to display a specific past order. """
    order = get_object_or_404(Order, order_number=order_number, user_profile__user=request.user)

    messages.info(request, f'Viewing past order: {order_number}')

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
