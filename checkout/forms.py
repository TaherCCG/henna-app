from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from .models import Order, Delivery

class OrderForm(forms.ModelForm):
    """
    Form for creating and updating orders. Includes fields for customer details
    and delivery options.
    """

    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town_or_city', 'postcode', 'country',
            'county', 'delivery_method',  
        )

    def __init__(self, *args, **kwargs):
        """
        Initialise the form, adding placeholders, custom classes, and autofocus.
        """
        total_cost = kwargs.pop('total_cost', None)
        super().__init__(*args, **kwargs)

        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        
        # Set placeholders and classes
        for field in self.fields:
            if field != 'delivery_method': 
                placeholder = placeholders[field]
                if self.fields[field].required:
                    placeholder += ' *'  
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].widget.attrs['class'] = 'stripe-style-input'
                self.fields[field].label = False

        # Get active delivery methods
        delivery_methods = Delivery.objects.filter(active=True)

        # Default to Standard Delivery
        if total_cost and total_cost >= settings.FREE_DELIVERY_THRESHOLD:
            free_delivery = delivery_methods.filter(name='Free Delivery').first()
            if free_delivery:
                self.fields['delivery_method'].initial = free_delivery.id
                self.fields['delivery_method'].queryset = delivery_methods.filter(name='Free Delivery')
            else:
                standard_delivery = delivery_methods.filter(name='Standard Delivery').first()
                if standard_delivery:
                    self.fields['delivery_method'].initial = standard_delivery.id
                    self.fields['delivery_method'].queryset = delivery_methods
        else:
            standard_delivery = delivery_methods.filter(name='Standard Delivery').first()
            if standard_delivery:
                self.fields['delivery_method'].initial = standard_delivery.id
                self.fields['delivery_method'].queryset = delivery_methods

        # Add custom class for the delivery method dropdown
        self.fields['delivery_method'].widget.attrs['class'] = 'stripe-style-input'
        self.fields['delivery_method'].empty_label = None


class DeliveryForm(forms.ModelForm):
    """
    Form for creating and updating delivery methods.
    """

    class Meta:
        model = Delivery
        fields = (
            'company_name', 'name', 'details', 'cost', 'estimated_delivery_time', 'active'
        )

    def __init__(self, *args, **kwargs):
        """
        Initialise the form, adding placeholders and custom classes.
        """
        super().__init__(*args, **kwargs)

        placeholders = {
            'company_name': 'Company Name',
            'name': 'Delivery Type Name',
            'details': 'Details about Delivery',
            'cost': 'Cost (£)',
            'estimated_delivery_time': 'Estimated Delivery Time',
        }

        # Set placeholders and classes
        for field in self.fields:
            if field in placeholders:
                placeholder = placeholders[field]
                if self.fields[field].required:
                    placeholder += ' *'
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].widget.attrs['class'] = 'stripe-style-input'
                self.fields[field].label = False

    def clean_name(self):
        """
        Validate that the delivery type name is unique and cannot be changed for certain methods.
        """
        name = self.cleaned_data.get('name')

        # Check if this is an update
        if self.instance.pk:  # Ensure this is an update and not a new delivery method
            current_name = Delivery.objects.get(pk=self.instance.pk).name
            if current_name in ['Free Delivery', 'Standard Delivery'] and name != current_name:
                raise ValidationError(
                    "The name of 'Free Delivery' and 'Standard Delivery' cannot be changed as they are used in other functions."
                )

        # Check for uniqueness
        if Delivery.objects.exclude(pk=self.instance.pk).filter(name=name).exists():
            raise ValidationError(f"A delivery method with the name '{name}' already exists.")
        
        return name

    def clean_cost(self):
        """
        Ensure that the cost is not below £0.
        """
        cost = self.cleaned_data.get('cost')
        if cost is not None and cost < 0:
            raise ValidationError("Delivery cost cannot be less than £0.")
        return cost


# References:
# Django Working with Forms: https://docs.djangoproject.com/en/5.1/topics/forms/#working-with-forms
# Accept a payment using Stripe Elements: https://docs.stripe.com/payments/accept-a-payment-charges#set-up-stripe-elements
