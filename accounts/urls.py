from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, TokenRefresh, UserProfileView, AddressViewSet, OTPRequestView, OTPVerifyView

router = DefaultRouter()
router.register(r'addresses', AddressViewSet, basename='address')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('otp/request/', OTPRequestView.as_view(), name='otp-request'),
    path('otp/verify/', OTPVerifyView.as_view(), name='otp-verify'),
    path('profile/', UserProfileView.as_view(), name='profile'),
] + router.urls