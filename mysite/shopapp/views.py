import os

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import FileUploadForm, OrderForm, ProductForm
from .models import Order, Product


def shop_index(request):
    return render(request, 'shopapp/index.html')


MAX_FILE_SIZE = 1 * 1024 * 1024


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = request.FILES['file']

            if uploaded_file.size > MAX_FILE_SIZE:
                messages.error(
                    request,
                    'Файл слишком большой. Максимальный размер: 1 MB.'
                )
                return redirect('shopapp:upload_file')

            os.makedirs('uploads', exist_ok=True)
            file_path = os.path.join('uploads', uploaded_file.name)

            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            messages.success(
                request,
                f'Файл «{uploaded_file.name}» успешно загружен!'
            )
            return redirect('shopapp:upload_file')
    else:
        form = FileUploadForm()

    return render(request, 'shopapp/upload_file.html', {'form': form})


class ProductListView(ListView):
    model = Product
    template_name = 'shopapp/products_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_archived=False)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shopapp/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shopapp/product_form.html'
    success_url = reverse_lazy('shopapp:products_list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shopapp/product_form.html'
    success_url = reverse_lazy('shopapp:products_list')


class ProductArchiveView(UpdateView):
    model = Product
    fields = []
    template_name = 'shopapp/product_archive_confirm.html'
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        form.instance.is_archived = True
        return super().form_valid(form)


class OrderListView(ListView):
    model = Order
    template_name = 'shopapp/orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return (
            Order.objects
            .select_related('customer')
            .prefetch_related('products')
        )


class OrderDetailView(DetailView):
    model = Order
    template_name = 'shopapp/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return (
            Order.objects
            .select_related('customer')
            .prefetch_related('products')
        )


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'shopapp/order_form.html'
    success_url = reverse_lazy('shopapp:orders_list')


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'shopapp/order_form.html'
    success_url = reverse_lazy('shopapp:orders_list')


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'shopapp/order_delete_confirm.html'
    context_object_name = 'order'
    success_url = reverse_lazy('shopapp:orders_list')
