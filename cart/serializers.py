from rest_framework import serializers
from .models import Cart, CartItem

class Cartsrializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['id', 'user', 'is_active', 'items', 'total_price']
        read_only_fields = ['id', 'user', 'total_price']


class CartItemSerializer(serializers.ModelSerializer):
    pass