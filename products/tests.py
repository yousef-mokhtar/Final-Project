from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product, Category

class ProductAPITest(APITestCase):

    def setUp(self):
        """
        ایجاد داده‌های تستی اولیه شامل دسته‌بندی و دو محصول.
        """
        self.category = Category.objects.create(name='تستی')
        self.product1 = Product.objects.create(name='محصول اول', category=self.category, brand='برند ۱')
        self.product2 = Product.objects.create(name='محصول دوم', category=self.category, brand='برند ۲', is_active=False)

    def test_list_products(self):
        """
        تست بررسی دریافت لیست محصولات.
        باید فقط محصولات فعال (active) را برگرداند.
        """
        url = reverse('product-list') 
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], self.product1.name)

    def test_retrieve_product_detail(self):
        """
        تست بررسی دریافت جزئیات یک محصول خاص.
        """
        url = reverse('product-detail', kwargs={'pk': self.product1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product1.name)
        self.assertEqual(response.data['brand'], self.product1.brand)

    def test_retrieve_inactive_product_fails(self):
        """
        تست می‌کند که آیا دسترسی به یک محصول غیرفعال خطای 404 برمی‌گرداند.
        """
        url = reverse('product-detail', kwargs={'pk': self.product2.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)