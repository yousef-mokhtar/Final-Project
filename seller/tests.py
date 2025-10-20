from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from .models import Store

class SellerTest(APITestCase):
    
    def setUp(self):
        self.user_data = {
            'email': 'test@test.com',
            'phone': '09123456789',
            'username': 'testuser',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)
    
    def test_register_as_seller(self):
        """
        تست می‌کند که آیا کاربر می‌تواند با موفقیت یک فروشگاه ثبت کند یا نه.
        """
        data = {
            'name': 'فروشگاه تست',
            'description': 'توضیحات تست برای فروشگاه جدید',
        }
        response = self.client.post('/api/myuser/register_as_seller/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Store.objects.count(), 1)
        store = Store.objects.first()
        self.assertEqual(store.name, 'فروشگاه تست')
        self.assertEqual(store.owner, self.user)
    
    def test_my_store_retrieve(self):
        """
        تست می‌کند که آیا فروشنده می‌تواند اطلاعات فروشگاه خود را مشاهده کند.
        """
        Store.objects.create(owner=self.user, name='فروشگاه من', description='توضیحات')
        
        response = self.client.get('/api/mystore/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'فروشگاه من')