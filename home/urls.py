from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'), 
    path('contact/', views.feedback_view, name='contact'),  
    path('contact/success/', views.feedback_success, name='feedback_success'),  
]