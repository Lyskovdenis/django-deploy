from rest_framework import serializers

from .models import Order, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'discount',
            'stock',
            'created_at',
            'is_available',
            'is_archived',
            'created_by',
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'customer',
            'products',
            'notes',
            'customer_name',
            'created_at',
        )