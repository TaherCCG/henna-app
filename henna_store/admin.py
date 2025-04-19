from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib import admin
from django.utils.html import format_html
from products.models import HennaProduct, ProductsCategory, Discount
from checkout.models import Delivery, Order, OrderItem
from profiles.models import UserProfile
from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site
from allauth.account.models import EmailAddress


class CustomAdminSite(AdminSite):
    site_header = "Henna Store Dashboard"
    site_title = "Henna Store Admin"
    index_title = "Welcome to the Henna Store Admin"


custom_admin_site = CustomAdminSite(name='custom_admin')


class DiscountInline(admin.TabularInline):
    model = HennaProduct.discounts.through
    extra = 1


class HennaProductAdmin(ModelAdmin):
    list_display = (
        'sku', 'name', 'category', 'price', 'get_discounted_price',
        'rating', 'stock_quantity', 'is_available', 'date_added',
        'display_image'
    )
    ordering = ('sku',)
    search_fields = ('name', 'sku', 'description', 'category__name')
    list_filter = ('category', 'is_available', 'date_added')
    inlines = [DiscountInline]
    date_hierarchy = 'date_added'
    actions = ['mark_as_unavailable']

    fieldsets = (
        (None, {'fields': ('sku', 'name', 'category')}),
        ('Pricing and Availability', {
            'fields': ('price', 'rating', 'stock_quantity', 'is_available')
        }),
        ('Additional Information', {
            'fields': ('date_added', 'description', 'image', 'image_url')
        }),
    )

    def mark_as_unavailable(self, request, queryset):
        queryset.update(is_available=False)

    def get_discounted_price(self, obj):
        return obj.get_discounted_price()

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />',
                               obj.image.url)
        return 'No Image'


class ProductsCategoryAdmin(ModelAdmin):
    list_display = ('friendly_name', 'name')
    search_fields = ('name', 'friendly_name')
    prepopulated_fields = {'friendly_name': ('name',)}
    fieldsets = (
        (None, {'fields': ('name', 'friendly_name')}),
    )


class DiscountAdmin(ModelAdmin):
    list_display = (
        'name', 'discount_type', 'value', 'start_date', 'end_date', 'active',
        'is_active_now'
    )
    search_fields = ('name',)
    list_filter = ('discount_type', 'active')

    fieldsets = (
        (None, {
            'fields': ('name', 'discount_type', 'value', 'start_date',
                       'end_date', 'active')
        }),
    )

    def is_active_now(self, obj):
        return obj.is_active()


class DeliveryAdmin(ModelAdmin):
    list_display = (
        'name', 'company_name', 'cost', 'active', 'estimated_delivery_time'
    )
    search_fields = ('name', 'company_name')
    list_filter = ('active',)
    fieldsets = (
        (None, {
            'fields': ('name', 'company_name', 'details', 'cost',
                       'estimated_delivery_time', 'active')
        }),
    )


class OrderAdmin(ModelAdmin):
    list_display = ('order_number', 'full_name', 'email', 'order_total',
                    'grand_total', 'date')
    search_fields = ('order_number', 'full_name', 'email')
    list_filter = ('date',)

    fieldsets = (
        (None, {
            'fields': ('order_number', 'user_profile', 'full_name', 'email',
                       'phone_number', 'street_address1', 'street_address2',
                       'town_or_city', 'postcode', 'county', 'country',
                       'date')
        }),
        ('Order Totals', {
            'fields': ('order_total', 'vat_amount', 'delivery_method',
                       'delivery_cost', 'grand_total', 'stripe_pid',
                       'original_cart')
        }),
    )


class OrderItemAdmin(ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price_at_order')
    search_fields = ('order__order_number', 'product__name')
    list_filter = ('order',)

    fieldsets = (
        (None, {'fields': ('order', 'product', 'quantity', 'price_at_order')}),
    )


class UserProfileAdmin(ModelAdmin):
    list_display = ('user', 'default_phone_number', 'default_town_or_city',
                    'default_country')
    search_fields = ('user__username', 'default_phone_number',
                     'default_town_or_city')

    fieldsets = (
        (None, {
            'fields': ('user', 'default_phone_number', 'default_street_address1',
                       'default_street_address2', 'default_town_or_city',
                       'default_postcode', 'default_county', 'default_country')
        }),
    )


custom_admin_site.register(HennaProduct, HennaProductAdmin)
custom_admin_site.register(ProductsCategory, ProductsCategoryAdmin)
custom_admin_site.register(Discount, DiscountAdmin)
custom_admin_site.register(Delivery, DeliveryAdmin)
custom_admin_site.register(Order, OrderAdmin)
custom_admin_site.register(OrderItem, OrderItemAdmin)
custom_admin_site.register(UserProfile, UserProfileAdmin)
custom_admin_site.register(User)
custom_admin_site.register(Group)
custom_admin_site.register(Site)

if EmailAddress:
    custom_admin_site.register(EmailAddress)
