from rest_framework import serializers
from .models import Store, StoreAddress, StoreItem
from products.serializers import ProductImageSerializer, CategorySerializer

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'owner', 'name', 'description', 'addresses']
        read_only_fields = ['id', 'owner']


class StoreItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product.name', read_only=True)
    description = serializers.CharField(source='product.description', read_only=True)

    class Meta:
        model = StoreItem
        fields = ['id', 'store', 'product', 'name', 'description', 'price', 'stock']
        read_only_fields = ['id']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('قیمت محصول باید مثبت باشد.')
        return value
    
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('موجودی نمی‌تواند منفی باشد.')
        

    def validation_information(self, request):
        pass

class StoreAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreAddress
        fields = ['id', 'title', 'province', 'city', 'postal_code', 'address_line', 'is_default']
        read_only_fields = ['id']

    def validate(self, attrs):
        if attrs.get('is_default'):
            store = self.context['view'].get_store_instance()
            store.addresses.filter(is_default=True).update(is_default=False)
        return attrs