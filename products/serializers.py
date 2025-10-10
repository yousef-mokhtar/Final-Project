from rest_framework import serializers
from django.db.models import Avg, Sum, Min
from seller.models import StoreItem
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
    

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text']
        read_only_fields = ['id']
    

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    
    rating = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()
    best_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 
            'category', 
            'name', 
            'description', 
            'brand', 
            'image',
            'images',
            'rating',     
            'stock',       
            'best_price',  
        ]

    def get_rating(self, obj):
        avg_rating = obj.product_reviews.filter(is_approved=True).aggregate(avg_rating=Avg('rating'))['avg_rating']
        return avg_rating if avg_rating is not None else 0

    def get_stock(self, obj):
        total_stock = StoreItem.objects.filter(product=obj, is_active=True).aggregate(total_stock=Sum('stock'))['total_stock']
        return total_stock if total_stock is not None else 0

    def get_best_price(self, obj):
        min_price = StoreItem.objects.filter(product=obj, is_active=True).aggregate(min_price=Min('price'))['min_price']
        return min_price