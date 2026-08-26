from django.shortcuts import render
from .models import Product, Order


def shop_index(request):
    return render(request, 'shopapp/index.html')


def products_list(request):
    products = Product.objects.all()
    return render(request, 'shopapp/products.html', {'products': products})


def orders_list(request):
    orders = Order.objects.all().select_related('customer').prefetch_related('products')
    return render(request, 'shopapp/orders.html', {'orders': orders})


def shop_view(request):
    products = Product.objects.all()
    return render(request, 'shopapp/shop.html', {'products': products})
