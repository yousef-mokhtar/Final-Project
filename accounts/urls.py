from django.urls import path
from .views import UserProfileView, RegisterView, OTPRequestView, OTPVerifyView, AddressViewSet
from seller.views import RegisterAsSellerView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'addresses', AddressViewSet, basename='address')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'), # قبلی
    path('myuser/', UserProfileView.as_view(), name='myuser'), # جدید
    path('otp/request/', OTPRequestView.as_view(), name='otp-request'),
    path('otp/verify/', OTPVerifyView.as_view(), name='verify-otp'),
    path('myuser/register_as_seller/', RegisterAsSellerView.as_view(), name='register_as_seller'), # این یکی الان مطابق لیست دوست هست
] + router.urls


# from django.urls import path
# from .views import RegisterView, OTPRequestView, OTPVerifyView

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('request-otp/', OTPRequestView.as_view(), name='otp-request'),
#     path('verify-otp/', OTPVerifyView.as_view(), name='otp-verify'),
# ]



# from django.urls import path

# from seller.views import RegisterAsSellerView
# from .views import RegisterView, LoginView, TokenRefresh, OTPRequestView, OTPVerifyView, UserProfileView, AddressViewSet

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('token/refresh/', TokenRefresh.as_view(), name='token_refresh'),
#     path('request-otp/', OTPRequestView.as_view(), name='request_otp'),
#     path('verify-otp/', OTPVerifyView.as_view(), name='verify_otp'),
#     path('myuser/', UserProfileView.as_view(), name='myuser'),
#     path('myuser/address/', AddressViewSet.as_view({'get': 'list', 'post': 'create'}), name='address_list'),
#     path('myuser/address/<int:pk>/', AddressViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='address_detail'),
#     path('myuser/register_as_seller/', RegisterAsSellerView.as_view(), name='register_as_seller'),
# ]