from django import forms
from .models import HennaProduct, ProductsCategory, Discount


# Product Form for managing Henna Products
class ProductForm(forms.ModelForm):
    class Meta:
        model = HennaProduct
        fields = [
            'sku', 'name', 'category', 'price', 'rating',
            'stock_quantity', 'is_available', 'description',
            'image', 'image_url'
        ]
        widgets = {
            'sku': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'SKU'}
            ),
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Product Name'}
            ),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Price'}
            ),
            'rating': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Rating'}
            ),
            'stock_quantity': forms.NumberInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Stock Quantity'}
            ),
            'is_available': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Product Description'}
            ),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(
                attrs={'class': 'form-control', 'placeholder': 'Image URL'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Replace the category field with friendly names
        categories = ProductsCategory.objects.all()
        friendly_names = [
            (category.id, category.get_friendly_name())
            for category in categories
        ]
        self.fields['category'].choices = friendly_names

        # Apply Bootstrap styling to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = field.widget.attrs.get(
                'class', ''
            ) + ' form-control'


# Discount Form for managing Discounts
class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = [
            'name', 'discount_type', 'value',
            'start_date', 'end_date', 'active'
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Discount Name'}
            ),
            'discount_type': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.NumberInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Discount Value'}
            ),
            'start_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'placeholder': 'Start Date'}
            ),
            'end_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'placeholder': 'End Date'}
            ),
            'active': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply Bootstrap styling to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = field.widget.attrs.get(
                'class', ''
            ) + ' form-control'
