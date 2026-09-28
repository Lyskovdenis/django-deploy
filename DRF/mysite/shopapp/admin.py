from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Order, Product


class OrderInline(admin.TabularInline):
    model = Order.products.through
    extra = 0
    verbose_name = _('order')
    verbose_name_plural = _('orders')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'discount',
        'stock',
        'is_available',
        'is_archived',
        'created_at',
    )
    search_fields = (
        'name',
        'description',
        'price',
        'discount',
    )
    list_filter = (
        'is_available',
        'is_archived',
        'created_at',
    )
    fieldsets = [
        (
            None,
            {
                'fields': (
                    'name',
                    'description',
                ),
            },
        ),
        (
            _('Price'),
            {
                'fields': (
                    'price',
                    'discount',
                ),
            },
        ),
        (
            _('Additional options'),
            {
                'fields': (
                    'stock',
                    'is_available',
                    'is_archived',
                    'created_at',
                ),
                'classes': ('collapse',),
            },
        ),
    ]
    inlines = [OrderInline]
    actions = ['archive_products']

    def archive_products(self, request, queryset):
        queryset.update(is_archived=True)

    archive_products.short_description = _(
        'Archive selected products',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',
        'customer',
        'created_at',
    )
    search_fields = (
        'customer_name',
        'customer__username',
        'notes',
    )
    filter_horizontal = ('products',)
