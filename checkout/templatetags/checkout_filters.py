from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def multiply(value, arg):
    """
    Multiplies the given value by the argument.
    Both value and arg are expected to be Decimals or values that can be cast to Decimals.
    """
    try:
        return Decimal(value) * Decimal(arg)
    except (ValueError, TypeError):
        return


# https://docs.djangoproject.com/en/5.1/howto/custom-template-tags/#creating-custom-template-filters