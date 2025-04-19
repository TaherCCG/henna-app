from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('update-delivery/<int:delivery_id>/', views.update_delivery, name='update_delivery'),
    path('checkout_success/<order_number>/', views.checkout_success, name='checkout_success'),
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
    path('wh/', views.stripe_webhook, name='webhook'),
    path('delivery/add/', views.add_delivery, name='add_delivery'),
    path('delivery/edit/<int:delivery_id>/', views.edit_delivery, name='edit_delivery'),
    path('delivery/<int:delivery_id>/delete/', views.delete_delivery, name='delete_delivery'),
    path('delivery/', views.list_deliveries, name='list_deliveries'),
]
