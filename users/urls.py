from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.user_home, name='user_home'),
    path('account/', views.account_view, name='account'),
    path('logout/', views.logout_view, name='logout'),


    path('products/', views.user_products, name='user_products'),
    path('delete-address/<int:id>/', views.delete_address, name='delete_address'),

    path('wishlist/add/<int:product_id>/', views.add_to_wishlist),
path('wishlist/', views.view_wishlist, name='wishlist'),
path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist),
path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist),
]