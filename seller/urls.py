from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MyStoreView, StoreItemViewSet, StoreAddressViewSet, StoreOrderItemViewSet

router = DefaultRouter()
router.register(r'items', StoreItemViewSet, basename='mystore-item')
router.register(r'address', StoreAddressViewSet, basename='mystore-address')

urlpatterns = [
    path('', MyStoreView.as_view(), name='mystore-detail'),
] + router.urls

# from django.urls import path
# from .views import RegisterAsSellerView, MyStoreView, StoreItemViewSet

# urlpatterns = [
#     path('seller_as_register/', RegisterAsSellerView.as_view(), name='seller_as_register'),
#     path('mystore/', MyStoreView.as_view(), name='mystore'),
#     path('mystore/items/', StoreItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='store_items_list'),
#     path('mystore/items/<int:pk>/', StoreItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='store_items_detail'),
# ]