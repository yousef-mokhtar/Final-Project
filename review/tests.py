from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from products.models import Product, Category
from .models import Review

class ReviewAPITest(APITestCase):

    def setUp(self):
        """
        ایجاد داده‌های تستی اولیه: یک کاربر و یک محصول.
        """
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='password123')
        self.category = Category.objects.create(name='تستی')
        self.product = Product.objects.create(name='محصول تستی', category=self.category)

    def test_create_review_authenticated(self):
        """
        تست می‌کند که آیا یک کاربر لاگین کرده می‌تواند نظر ثبت کند.
        """
        self.client.force_authenticate(user=self.user)
        
        url = reverse('product-reviews-list', kwargs={'product_pk': self.product.pk})
        
        data = {
            'rating': 5,
            'text': 'این یک محصول عالی است!'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        review = Review.objects.first()
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.rating, 5)

    def test_create_review_unauthenticated(self):
        """
        تست می‌کند که آیا کاربر مهمان (لاگین نکرده) نمی‌تواند نظر ثبت کند.
        """
        url = reverse('product-reviews-list', kwargs={'product_pk': self.product.pk})
        data = {'rating': 4, 'text': 'نظر تستی'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Review.objects.count(), 0)

    def test_create_duplicate_review_fails(self):
        """
        تست می‌کند که آیا یک کاربر نمی‌تواند برای یک محصول دو بار نظر ثبت کند.
        """
        Review.objects.create(user=self.user, product=self.product, rating=5, text='نظر اول')

        self.client.force_authenticate(user=self.user)
        url = reverse('product-reviews-list', kwargs={'product_pk': self.product.pk})
        data = {'rating': 3, 'text': 'نظر دوم'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.count(), 1) 