import json

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, Client
from django.urls import reverse

from .models import Order, Product


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём пользователя
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
        )
        # Выдаём право на просмотр заказа
        content_type = ContentType.objects.get_for_model(Order)
        permission, _ = Permission.objects.get_or_create(
            codename='view_order',
            content_type=content_type,
            defaults={'name': 'Can view order'},
        )
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        # Удаляем пользователя
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        # Вход пользователя
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

        # Создаём заказ для теста
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=100.00,
            stock=10,
            created_by=self.user,
        )
        self.order = Order.objects.create(
            customer=self.user,
            customer_name='Test Customer',
            notes='Promo: TEST2026',
        )
        self.order.products.add(self.product)

    def tearDown(self):
        # Удаляем заказ после теста
        self.order.delete()
        self.product.delete()

    def test_order_details(self):
        response = self.client.get(reverse('shopapp:order_detail', args=[self.order.pk]))

        # Проверка статуса
        self.assertEqual(response.status_code, 200)

        # Проверка, что в теле ответа есть адрес заказа (customer_name)
        self.assertContains(response, self.order.customer_name)

        # Проверка, что в теле ответа есть промокод (в notes)
        self.assertContains(response, 'Promo: TEST2026')

        # Проверка, что в контексте тот же заказ
        self.assertEqual(response.context['order'].pk, self.order.pk)


class OrdersExportTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём staff пользователя
        cls.staff_user = User.objects.create_user(
            username='staffuser',
            password='staffpass123',
            email='staff@example.com',
            is_staff=True,
        )

    @classmethod
    def tearDownClass(cls):
        # Удаляем пользователя
        cls.staff_user.delete()
        super().tearDownClass()

    def setUp(self):
        # Вход пользователя
        self.client = Client()
        self.client.login(username='staffuser', password='staffpass123')

        # Создаём тестовые данные
        self.product1 = Product.objects.create(
            name='Product 1',
            description='Desc 1',
            price=50.00,
            stock=5,
            created_by=self.staff_user,
        )
        self.product2 = Product.objects.create(
            name='Product 2',
            description='Desc 2',
            price=75.00,
            stock=3,
            created_by=self.staff_user,
        )

        self.order1 = Order.objects.create(
            customer=self.staff_user,
            customer_name='Address 1',
            notes='PROMO1',
        )
        self.order1.products.add(self.product1, self.product2)

        self.order2 = Order.objects.create(
            customer=self.staff_user,
            customer_name='Address 2',
            notes='PROMO2',
        )
        self.order2.products.add(self.product1)

    def tearDown(self):
        # Очищаем данные после теста
        self.order1.delete()
        self.order2.delete()
        self.product1.delete()
        self.product2.delete()

    def test_export_orders(self):
        response = self.client.get(reverse('shopapp:orders_export'))

        # Проверка статуса
        self.assertEqual(response.status_code, 200)

        # Проверка, что ответ JSON
        self.assertEqual(response['Content-Type'], 'application/json')

        # Парсим JSON
        data = json.loads(response.content)

        # Проверка, что есть ключ orders
        self.assertIn('orders', data)
        self.assertEqual(len(data['orders']), 2)

        # Проверка структуры данных
        order_ids = {order['id'] for order in data['orders']}
        self.assertIn(self.order1.id, order_ids)
        self.assertIn(self.order2.id, order_ids)

        # Проверка полей первого заказа
        order1_data = next(o for o in data['orders'] if o['id'] == self.order1.id)
        self.assertEqual(order1_data['address'], 'Address 1')
        self.assertEqual(order1_data['promo_code'], 'PROMO1')
        self.assertEqual(order1_data['user_id'], self.staff_user.id)
        self.assertEqual(set(order1_data['product_ids']), {self.product1.id, self.product2.id})
