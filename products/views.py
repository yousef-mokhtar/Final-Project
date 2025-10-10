from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from accounts.models import User
from accounts.serializers import UserSerializer
from .models import Category, Product, ProductImage
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    این ViewSet فقط برای خواندن (GET) لیست و جزئیات دسته‌بندی‌هاست.
    """
    queryset = Category.objects.filter(is_active=True, is_deleted=False)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None 


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    این ViewSet فقط برای خواندن (GET) لیست و جزئیات محصولات است.
    """
    queryset = Product.objects.filter(is_active=True, is_deleted=False)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description', 'brand']
    ordering_fields = ['created_at', 'name']

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.filter(product__is_deleted=False)
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'], product__is_deleted=False)
    
class AdminCategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class AdminProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]