from rest_framework import serializers
from .models import Cart, CartItem
from seller.serializers import StoreItemSerializer
from seller.models import StoreItem


class CartItemSerializer(serializers.ModelSerializer):
    store_item = StoreItemSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'store_item', 'quantity', 'total_price']
        read_only_fields = ['id', 'total_price']

    def validate_quantity(self, value):
        store_item_id = self.initial_data.get('store_item')

        if not store_item_id:
            raise serializers.ValidationError("محصول انتخاب نشده است.")

        try:
            store_item = StoreItem.objects.get(id=store_item_id)
        except StoreItem.DoesNotExist:
            raise serializers.ValidationError("محصول موردنظر وجود ندارد.")

        if value > store_item.stock:
            raise serializers.ValidationError("موجودی کافی نیست.")

        return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'is_active', 'items', 'total_price']
        read_only_fields = ['id', 'user', 'total_price']