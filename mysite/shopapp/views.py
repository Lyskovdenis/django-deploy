from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Order
from .forms import FileUploadForm, ProductForm, OrderForm
import os

MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB в байтах


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


def upload_file(request):
    """View для загрузки файлов с ограничением по размеру"""
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            if uploaded_file.size > MAX_FILE_SIZE:
                messages.error(request, 'Файл слишком большой! Максимальный размер: 1 MB')
                return redirect('shopapp:upload_file')

            file_path = os.path.join('uploads', uploaded_file.name)
            os.makedirs('uploads', exist_ok=True)

            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            messages.success(request, f'Файл {uploaded_file.name} успешно загружен!')
            return redirect('shopapp:upload_file')
    else:
        form = FileUploadForm()

    return render(request, 'shopapp/upload_file.html', {'form': form})


def create_product(request):
    """View для создания продукта"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт успешно создан!')
            return redirect('shopapp:products')
    else:
        form = ProductForm()

    return render(request, 'shopapp/create_product.html', {'form': form})


def create_order(request):
    """View для создания заказа"""
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заказ успешно создан!')
            return redirect('shopapp:orders')
    else:
        form = OrderForm()

    return render(request, 'shopapp/create_order.html', {'form': form})
