from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from .models import Store
from .serializers import StoreSerializer

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
        data = {
            'name': 'فروشگاه تست',
            'description': 'توضیحات',
            'address': 'آدرس تست'
        }
        response = self.client.post('/api/seller/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Store.objects.count(), 1)
        store = Store.objects.first()
        self.assertEqual(store.name, 'فروشگاه تست')
        self.assertEqual(store.owner, self.user)
    
    def test_my_store(self):
        store = Store.objects.create(owner=self.user, name='فروشگاه من', description='توضیحات', address='آدرس')
        response = self.client.get('/api/seller/my-store/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'فروشگاه من')