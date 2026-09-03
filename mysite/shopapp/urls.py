from django.urls import path
from . import views

app_name = 'shopapp'

urlpatterns = [
    path('', views.shop_index, name='index'),
    path('products/', views.products_list, name='products'),
    path('orders/', views.orders_list, name='orders'),
    path('shop/', views.shop_view, name='shop'),
    path('upload/', views.upload_file, name='upload_file'),
    path('products/create/', views.create_product, name='create_product'),
    path('orders/create/', views.create_order, name='create_order'),
]
