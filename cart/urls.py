from django.urls import path
from .views import CartView, AddToCartView, CartItemViewSet

urlpatterns = [
    path('mycart/', CartView.as_view(), name='mycart'),
    path('mycart/add_to_cart/<int:store_item_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('mycart/items/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='cart_items_list'),
    path('mycart/items/<int:pk>/', CartItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='cart_items_detail'),
]