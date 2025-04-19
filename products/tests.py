from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError 
from decimal import Decimal
from products.models import ProductsCategory, Discount, HennaProduct


class DiscountModelTest(TestCase):
    """Test suite for the Discount model."""

    def setUp(self):
        """Set up a discount object for testing."""
        self.discount = Discount.objects.create(
            name='10% Off',
            discount_type='percentage',
            value=Decimal('10.00'),
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=10)
        )

    def test_discount_creation(self):
        """Test that the discount object is created correctly."""
        self.assertEqual(self.discount.name, '10% Off')
        self.assertEqual(self.discount.discount_type, 'percentage')
        self.assertEqual(self.discount.value, Decimal('10.00'))

    def test_discount_string_representation(self):
        """Test the string representation of the discount object."""
        self.assertEqual(str(self.discount), '10% Off (Percentage)')

    def test_discount_validation_negative_value(self):
        """Test that a negative discount value raises a ValidationError."""
        with self.assertRaises(ValidationError):
            discount = Discount(name='Invalid Discount', discount_type='fixed', value=Decimal('-5.00'))
            discount.clean()

    def test_discount_is_active(self):
        """Test the is_active method for the discount."""
        self.assertTrue(self.discount.is_active())
        self.discount.active = False
        self.assertFalse(self.discount.is_active())
        self.discount.active = True
        self.discount.end_date = timezone.now() - timezone.timedelta(days=1)  # Make it inactive
        self.assertFalse(self.discount.is_active())


class DiscountModelFutureDateTest(TestCase):
    """Test suite for discounts starting in the future."""

    def setUp(self):
        """Set up a future discount object for testing."""
        self.discount = Discount.objects.create(
            name='Future Discount',
            discount_type='percentage',
            value=Decimal('10.00'),
            start_date=timezone.now() + timezone.timedelta(days=10),  # Starts in the future
            end_date=timezone.now() + timezone.timedelta(days=20)
        )

    def test_future_discount_is_not_active(self):
        """Test that a future discount is not active."""
        self.assertFalse(self.discount.is_active())  # Should not be active since it's in the future


class ProductsCategoryModelTest(TestCase):
    """Test suite for the ProductsCategory model."""

    def setUp(self):
        """Set up a product category object for testing."""
        self.category = ProductsCategory.objects.create(name='Henna', friendly_name='Henna Products')

    def test_category_creation(self):
        """Test that the product category object is created correctly."""
        self.assertEqual(self.category.name, 'Henna')
        self.assertEqual(self.category.friendly_name, 'Henna Products')

    def test_category_string_representation(self):
        """Test the string representation of the product category object."""
        self.assertEqual(str(self.category), 'Henna')

    def test_get_friendly_name(self):
        """Test the retrieval of the friendly name for the category."""
        self.assertEqual(self.category.get_friendly_name(), 'Henna Products')
        self.category.friendly_name = None
        self.assertEqual(self.category.get_friendly_name(), 'Henna')
