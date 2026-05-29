from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('orders/', views.owner_orders, name='owner_orders'),
    
path('accept/<int:order_id>/', views.accept_order, name='accept_order'),
path('reject/<int:order_id>/', views.reject_order, name='reject_order'),

path('products/', views.owner_products, name='owner_products'),
]