import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum, F, DecimalField
from django_countries.fields import CountryField
from products.models import HennaProduct
from profiles.models import UserProfile


class Delivery(models.Model):
    """
    Model representing delivery methods.
    Includes company name, cost, and estimated delivery time.
    """
    company_name = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    details = models.TextField()
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    estimated_delivery_time = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Model representing a customer's order, including VAT, delivery cost, and grand total.
    """
    order_number = models.CharField(max_length=32, null=False, editable=False, unique=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, 
                                     blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    county = models.CharField(max_length=80, null=True, blank=True)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    vat_amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    delivery_method = models.ForeignKey(Delivery, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    grand_total_with_vat = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID.
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the save method to assign an order number if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)  # Save the order first
        self.update_total()  # Then update totals after saving

    def update_total(self):
        """
        Update the grand total for the order, considering VAT, discounts, and delivery costs.
        """
        # Calculate the total price of all items, factoring in their quantities
        self.order_total = self.orderitems.aggregate(
            total=Sum(F('price_at_order') * F('quantity'), output_field=DecimalField())
        )['total'] or Decimal('0.00')

        # Fetch delivery cost if method is selected
        if self.delivery_method:
            self.delivery_cost = self.delivery_method.cost

        # Calculate VAT (Assuming a VAT_RATE constant in settings)
        vat_rate = Decimal(settings.VAT_RATE)
        self.vat_amount = (self.order_total * vat_rate).quantize(Decimal('0.01'))

        # Calculate grand total (order total + delivery cost)
        self.grand_total = self.order_total + self.delivery_cost

        # Calculate grand total including VAT
        self.grand_total_with_vat = (self.grand_total + self.vat_amount).quantize(Decimal('0.01'))

        # Save changes to the totals
        super().save(update_fields=['order_total', 'grand_total', 'vat_amount', 'grand_total_with_vat', 'delivery_cost'])


class OrderItem(models.Model):
    """
    Model representing an individual item in an order.
    """
    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE)
    product = models.ForeignKey(HennaProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        """
        Override save to set the price at order time, considering any active discounts.
        """
        if self.price_at_order == 0.00:
            self.price_at_order = self.product.get_discounted_price()
        super().save(*args, **kwargs)

    def get_total(self):
        """
        Calculate the total price for this item (quantity * price_at_order).
        """
        return self.price_at_order * self.quantity

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
