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
            'created_at',
            'archived',
            'preview',
        )
        read_only_fields = (
            'id',
            'created_at',
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'delivery_address',
            'promocode',
            'created_at',
            'user',
            'products',
            'receipt',
        )
        read_only_fields = (
            'id',
            'created_at',
        )