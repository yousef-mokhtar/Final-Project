from rest_framework import serializers
from .models import Store, StoreItem
from products.serializers import ProductImageSerializer, CategorySerializer

class StoreSerialize(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'owner', 'name', 'description', 'address']
        read_only_fields = ['id', 'owner']