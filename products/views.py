from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Category, Product, ProductImage
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_deleted=False)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if  self.action in ['create', 'update', 'destroy']:
              return [IsAdminUser()]
        return [AllowAny()]
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    class ProductViewSet(viewsets.ModelViewSet):
      queryset = Product.objects.filter(is_deleted=False)
      serializer_class = ProductSerializer
      permission_classes = [AllowAny]

      def get_permissions(self):
            if self.action in ['create', 'update', 'destroy']:
              return [IsAdminUser()]
            return [AllowAny()]
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.filter(product__is_deleted=False)
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'], product__is_deleted=False)