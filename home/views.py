from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import ContactUsForm
from products.models import HennaProduct


def index(request):
    """Get the top 6 most-rated products."""

    # Clear feedback session variables if they exist
    request.session.pop('feedback_sender_name', None)
    request.session.pop('feedback_contact_method', None)

    top_rated_products = HennaProduct.objects.filter(rating__isnull=False) \
        .order_by('-rating')[:6]

    context = {
        'products': top_rated_products,
    }
    return render(request, 'home/index.html', context)


def feedback_view(request):
    """View to handle contact form submission and send email."""
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            reason = form.cleaned_data['reason']
            contact_method = form.cleaned_data['contact_method']

            # Email content
            email_message = (
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone: {phone if phone else 'Not Provided'}\n"
                f"Subject: {subject}\n"
                f"Message: {message}\n"
                f"Reason for Contact: {reason}\n"
                f"Preferred Contact Method: {contact_method}\n"
            )

            # Send email
            send_mail(
                f'New Contact Form Submission: {subject}',
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                ['ccg.devops@gmail.com'],
                fail_silently=False,
            )

            # Store the name and preferred contact method in the session
            request.session['feedback_sender_name'] = name
            request.session['feedback_contact_method'] = contact_method

            return redirect('feedback_success')
    else:
        form = ContactUsForm()

    return render(request, 'home/feedback_form.html', {'form': form})


def feedback_success(request):
    """Feedback success page."""
    feedback_sender_name = request.session.get('feedback_sender_name', 'Guest')
    feedback_contact_method = request.session.get(
        'feedback_contact_method', 'Not Provided'
    )

    return render(request, 'home/feedback_success.html', {
        'feedback_sender_name': feedback_sender_name,
        'feedback_contact_method': feedback_contact_method
    })
