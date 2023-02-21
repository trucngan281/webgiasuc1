from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_page, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('add-to-cart/<pk>/', views.add_to_cart, name='add-to-cart'),
    path('minus-to-cart/<pk>/', views.minus_to_cart, name='minus-to-cart'),
    path('remove-from-cart/<pk>/', views.remove_from_cart, name='remove-from-cart')
]
