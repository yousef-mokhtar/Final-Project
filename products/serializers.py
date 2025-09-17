from rest_framework import serializers
from .models import Category, Product, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError('این نام دسته‌بندی قبلاً وجود دارد.')
        return value
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'brand', 'image', 'images']
        read_only_fields = ['id']

    def validate(self, data):
        if not data.get('name') or not data.get('description'):
            raise serializers.ValidationError('نام و توضیحات محصول الزامی است.')
        return data
    

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text']
        read_only_fields = ['id']