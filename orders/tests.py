# orders/tests.py (نسخه نهایی و اصلاح شده)

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User, Address
from seller.models import Store, StoreItem
from products.models import Product, Category
from cart.models import Cart, CartItem
from .models import Order, OrderItem

class CartAndCheckoutTest(APITestCase):

    def setUp(self):
        """
        آماده‌سازی داده‌های اولیه برای تمام تست‌ها.
        این داده‌ها شامل کاربر خریدار, فروشنده, فروشگاه, محصول و آدرس است.
        """
        # 1. ساخت کاربر خریدار
        self.user = User.objects.create_user(
            username='buyer',
            email='buyer@test.com',
            password='password123',
            phone='09120000000'
        )
        self.address = Address.objects.create(
            user=self.user,
            title='محل کار',
            province='تهران',
            city='تهران',
            postal_code='1111111111',
            address_line='خ تست'
        )

        # 2. ساخت کاربر فروشنده و فروشگاه او
        self.seller_user = User.objects.create_user(
            username='seller',
            email='seller@test.com',
            password='password123',
            phone='09121111111'
        )
        self.store = Store.objects.create(owner=self.seller_user, name='فروشگاه فروشنده')
        
        # 3. ساخت محصول و آیتم فروشگاه
        self.category = Category.objects.create(name='الکترونیک')
        self.product = Product.objects.create(name='لپتاپ', category=self.category)
        self.store_item = StoreItem.objects.create(
            store=self.store,
            product=self.product,
            price=50000,
            stock=10
        )

    def test_add_to_cart_and_view_cart(self):
        """
        تست می‌کند که آیا کاربر می‌تواند محصولی را به سبد خرید اضافه کرده و محتوای سبد را ببیند.
        """
        # احراز هویت به عنوان کاربر خریدار
        self.client.force_authenticate(user=self.user)

        # افزودن محصول به سبد خرید (API شما از POST روی items استفاده می‌کند)
        add_to_cart_url = reverse('cart_items_list')
        data = {'store_item': self.store_item.id, 'quantity': 2}
        response = self.client.post(add_to_cart_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)
        
        # بررسی محتوای سبد خرید
        view_cart_url = reverse('mycart')
        response = self.client.get(view_cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # بررسی اینکه آیا قیمت کل سبد خرید به درستی محاسبه شده است
        expected_total = self.store_item.price * 2
        
        # === خط اصلاح شده ===
        # هر دو مقدار به عدد صحیح (int) تبدیل می‌شوند تا از خطای نوع داده جلوگیری شود.
        self.assertEqual(int(response.data['total_price']), int(expected_total))
        # ======================

        self.assertEqual(len(response.data['items']), 1)

    def test_checkout_process_creates_order(self):
        """
        تست کامل فرآیند Checkout: از سبد خرید پر تا ایجاد سفارش.
        """
        # ابتدا یک آیتم به سبد خرید کاربر اضافه می‌کنیم
        cart, _ = Cart.objects.get_or_create(user=self.user)
        CartItem.objects.create(cart=cart, store_item=self.store_item, quantity=3)

        # احراز هویت به عنوان کاربر خریدار
        self.client.force_authenticate(user=self.user)
        
        # اجرای فرآیند Checkout
        checkout_url = reverse('checkout')
        checkout_data = {'shipping_address': self.address.id}
        response = self.client.post(checkout_url, checkout_data)

        # بررسی نتایج
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('payment_url', response.data)

        # بررسی اینکه آیا سفارش و آیتم سفارش در دیتابیس ساخته شده‌اند
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

        # بررسی جزئیات سفارش ساخته شده
        order = Order.objects.first()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.shipping_address, self.address)
        
        # بررسی قیمت نهایی سفارش
        expected_total = self.store_item.price * 3

        # === خط اصلاح شده ===
        # اینجا هم برای هماهنگی و اطمینان، هر دو مقدار را به عدد صحیح تبدیل می‌کنیم.
        self.assertEqual(int(order.total_price), int(expected_total))
        # ======================
        
        # بررسی اینکه سبد خرید پس از Checkout غیرفعال شده است
        cart.refresh_from_db()
        self.assertFalse(cart.is_active)