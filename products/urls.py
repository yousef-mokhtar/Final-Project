from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()

router.register(r'', ProductViewSet, basename='product')

urlpatterns = router.urls


# from django.urls import path
# from .views import CategoryViewSet, ProductViewSet

# urlpatterns = [
#     path('categories/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='categories_list'),
#     path('categories/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='categories_detail'),
#     path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='products_list'),
#     path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='products_detail'),
# ]