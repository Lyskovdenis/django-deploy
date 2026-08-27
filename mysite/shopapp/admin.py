from django.contrib import admin
from .models import Product, Order


class OrderInline(admin.TabularInline):
    model = Order.products.through
    extra = 0
    verbose_name = 'Заказ'
    verbose_name_plural = 'Заказы'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Поля для отображения в списке
    list_display = ('name', 'price', 'discount', 'stock', 'is_available', 'is_archived', 'created_at')

    # Поиск по полям
    search_fields = ('name', 'description', 'price', 'discount')

    # Фильтры
    list_filter = ('is_available', 'is_archived', 'created_at')

    # Группировка полей
    fieldsets = [
        (None, {
            'fields': ('name', 'description'),
        }),
        ('Цена', {
            'fields': ('price', 'discount'),
        }),
        ('Дополнительные опции', {
            'fields': ('stock', 'is_available', 'is_archived', 'created_at'),
            'classes': ('collapse',),  # Свёрнутая секция
        }),
    ]

    # Отображение связи "ко многим"
    inlines = [OrderInline]

    # Групповое действие
    actions = ['archive_products']

    def archive_products(self, request, queryset):
        queryset.update(is_archived=True)

    archive_products.short_description = 'Архивировать выбранные продукты'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer', 'created_at')
    search_fields = ('customer_name', 'customer__username', 'notes')
    filter_horizontal = ('products',)
