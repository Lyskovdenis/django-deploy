from django import forms
from .models import Product, Order


class FileUploadForm(forms.Form):
    file = forms.FileField(label='Выберите файл')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'discount', 'stock', 'is_available']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'price': 'Цена',
            'discount': 'Скидка',
            'stock': 'Количество на складе',
            'is_available': 'Доступен',
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'products']
        labels = {
            'customer': 'Клиент',
            'products': 'Продукты',
        }
