from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F, Case, When, Value, PositiveSmallIntegerField
from .models import Category, Order, OrderDetail, Product
from django.contrib import messages


def shop_page(request):
    category = Category.objects.all()
    products = Product.objects.filter(is_draft=False)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'shop/shop.html', context)


def product_details(request, product_id):
    product_details = Product.objects.get(id=product_id)
    ctg = Category.objects.get(name=product_details.category)
    related_products = Product.objects.filter(category=ctg)
    currently_order_quantity = product_details.get_current_quantity(
        request.user)
    print(currently_order_quantity)
    context = {
        'product': product_details,
        'related_products': related_products,
        'currently_order_quantity': currently_order_quantity
    }
    return render(request, 'shop/product-details.html', context)


def wishlist(request):
    return render(request, 'shop/wishlist.html')
