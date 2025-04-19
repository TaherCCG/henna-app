from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),  
    path('product/add/', views.add_product, name='add_product'),  
    path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),  
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),  
    path('discount/add/', views.add_discount, name='add_discount'),  
    path('discount/edit/<int:discount_id>/', views.edit_discount, name='edit_discount'), 
    path('discount/delete/<int:discount_id>/', views.delete_discount, name='delete_discount'),  
]
