from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MyOrderView, CheckoutView, VerifyPaymentView, AdminOrderViewSet

router = DefaultRouter()
router.register(r'myorders', MyOrderView, basename='myorders')
router.register(r'admin/orders', AdminOrderViewSet, basename='admin-orders')

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('verify/', VerifyPaymentView.as_view(), name='verify-payment'),
] + router.urls


# from django.urls import path
# from .views import (MyOrderView,CheckoutView,VerifyPaymentView,AdminOrderViewSet,)

# urlpatterns = [
#     path('my-orders/',MyOrderView.as_view({'get': 'list', 'retrieve': 'retrieve'}),name='my-orders'),
#     path('checkout/',CheckoutView.as_view(),name='checkout'),
#     path('verify/',VerifyPaymentView.as_view(),name='verify-payment'),
#     path('admin/',AdminOrderViewSet.as_view({'get': 'list', 'post': 'create'}),name='admin-order-list-create'),
#     path('admin/<int:pk>/',AdminOrderViewSet.as_view({'get': 'retrieve','put': 'update','patch': 'partial_update','delete': 'destroy'}),name='admin-order-detail'),]
