from rest_framework import serializers
from .models import Cart, CartItem
from seller.serializers import StoreItemSerializer

class Cartsrializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['id', 'user', 'is_active', 'items', 'total_price']
        read_only_fields = ['id', 'user', 'total_price']


class CartItemSerializer(serializers.ModelSerializer):
    store_item = StoreItemSerializer(read_only=True)
    total_price = serializers.ReadOnlyField(many=True)

    class Meta:
        model = CartItem
        fields = ['id', 'store_item', 'quantity', 'total_price']
        read_only_fields = ['id', 'total_price']