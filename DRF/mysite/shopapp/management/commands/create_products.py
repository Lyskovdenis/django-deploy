from django.core.management.base import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    help = 'Создаёт тестовые продукты'

    def handle(self, *args, **options):
        products = [
            {'name': 'Ноутбук', 'description': 'Мощный ноутбук', 'price': '99999.99', 'stock': 10},
            {'name': 'Смартфон', 'description': 'Современный смартфон', 'price': '49999.99', 'stock': 20},
            {'name': 'Наушники', 'description': 'Беспроводные наушники', 'price': '4999.99', 'stock': 50},
        ]

        for prod in products:
            product, created = Product.objects.get_or_create(
                name=prod['name'],
                defaults=prod
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создан продукт: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Продукт уже существует: {product.name}'))
