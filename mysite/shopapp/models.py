from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )
    stock = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    is_available = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_('Created by'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        permissions = [
            ('can_create_product', _('Can create products')),
            ('can_edit_product', _('Can edit products')),
        ]

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    notes = models.TextField(blank=True)
    customer_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return f'Order {self.id} by {self.customer_name}'
