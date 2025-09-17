from rest_framework import serializers
from .models import Store, StoreItem
from products.serializers import ProductImageSerializer, CategorySerializer

class StoreSerialize(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'owner', 'name', 'description', 'address']
        read_only_fields = ['id', 'owner']


class StoreItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreItem
        fields = ['id', 'store', 'product', 'category', 'name', 'description', 'price', 'stock']
        read_only_fields = ['id']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('مبلغ پرداخت باید مثبت باشد.')
        return value
    
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('موجودی نمی‌تواند منفی باشد.')