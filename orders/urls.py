from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase/<int:cart_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:cart_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('history/', views.order_history, name='order_history'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]