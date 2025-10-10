from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserProfileView, AddressViewSet
from seller.views import RegisterAsSellerView

router = DefaultRouter()
router.register(r'address', AddressViewSet, basename='myuser-address')

urlpatterns = [
    path('', UserProfileView.as_view(), name='myuser-profile'),

    path('register_as_seller/', RegisterAsSellerView.as_view(), name='myuser-register-seller'),
]

urlpatterns += router.urls