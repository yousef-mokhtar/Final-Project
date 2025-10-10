from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, StartPaymentView, VerifyPaymentView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('payments/<int:id>/start/', StartPaymentView.as_view(), name='start-payment'),
    path('payments/verify/', VerifyPaymentView.as_view(), name='verify-payment'),
] + router.urls



# from django.urls import path
# from .views import PaymentViewSet, StartPaymentView

# payment_list = PaymentViewSet.as_view({'get': 'list', 'post': 'create'})
# payment_detail = PaymentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})  

# urlpatterns = [
#     path('payments/', payment_list, name='payments-list'),
#     path('payments/<int:pk>/', payment_detail, name='payments-detail'),
#     path('payments/<int:pk>/start/', StartPaymentView.as_view(), name='start-payment'),
# ]