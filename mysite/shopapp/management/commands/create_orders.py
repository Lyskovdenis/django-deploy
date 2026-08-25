from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Product, Order


class Command(BaseCommand):
    help = 'Создаёт тестовые заказы'

    def handle(self, *args, **options):
        # Получаем или создаём пользователя
        user, _ = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com'}
        )

        # Получаем продукты
        products = Product.objects.all()[:2]

        # Создаём заказ
        order, created = Order.objects.get_or_create(
            customer=user,
            customer_name='Тестовый пользователь',
            defaults={'notes': 'Тестовый заказ'}
        )

        if created:
            order.products.set(products)
            self.stdout.write(self.style.SUCCESS(f'Создан заказ: {order.id}'))
        else:
            self.stdout.write(self.style.WARNING(f'Заказ уже существует: {order.id}'))