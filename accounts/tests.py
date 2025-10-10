from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Address
from .serializers import UserSerializer, AddressSerializer

class AccountsTest(APITestCase):

    def setUp(self):
        self.user_data = {
            'email': 'test@test.com',
            'phone': '09123456789',
            'username': 'testuser',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
    
    def test_register(self):
        response = self.client.post('/api/accounts/register/', self.user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.email, 'test@test.com')
        self.assertFalse(user.is_verified)
    
    def test_login(self):
        User.objects.create_user(**self.user_data)
        login_data = {'email': 'test@test.com', 'password': 'testpass123'}
        response = self.client.post('/api/token/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_address_create(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        address_data = {
            'title': 'خانه',
            'province': 'تهران',
            'city': 'تهران',
            'postal_code': '1234567890',
            'address_line': 'خیابان تست'
        }
        response = self.client.post('/api/accounts/addresses/', address_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.count(), 1)