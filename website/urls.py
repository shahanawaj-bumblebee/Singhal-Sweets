from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('product/<int:id>/', views.product_detail, name="product_detail"),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('cart/', views.cart, name="cart"),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name="remove_from_cart"),
    path('update/<int:item_id>/<str:action>/', views.update_quantity, name='update_quantity'),

    path('checkout/', views.checkout, name="checkout"),

    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
]