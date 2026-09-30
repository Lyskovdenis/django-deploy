from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        'name',
        'description',
    ]

    ordering_fields = [
        'id',
        'name',
        'price',
        'discount',
        'stock',
        'created_at',
    ]

    ordering = [
        'id',
    ]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_fields = [
        'customer',
        'customer_name',
        'products',
        'created_at',
    ]

    ordering_fields = [
        'id',
        'customer_name',
        'created_at',
    ]

    ordering = [
        '-created_at',
    ]