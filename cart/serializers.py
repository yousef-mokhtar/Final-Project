from rest_framework import serializers
from .models import Cart, CartItem
from seller.serializers import StoreItemSerializer  
from seller.models import StoreItem

class CartItemSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای آیتم‌های سبد خرید.
    - هنگام خواندن (GET)، جزئیات کامل محصول را نمایش می‌دهد.
    - هنگام نوشتن (POST/PUT)، فقط ID محصول را دریافت می‌کند.
    """

    store_item_details = StoreItemSerializer(source='store_item', read_only=True)

    store_item = serializers.PrimaryKeyRelatedField(
        queryset=StoreItem.objects.all(),
        write_only=True
    )

    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = [
            'id',
            'store_item',          
            'store_item_details', 
            'quantity',
            'total_price'
        ]
        read_only_fields = ['id', 'total_price']

    def validate_quantity(self, value):
        store_item_id = self.initial_data.get('store_item')

        if self.instance and not store_item_id:
            store_item = self.instance.store_item
        else:
            try:
                store_item = StoreItem.objects.get(id=store_item_id)
            except StoreItem.DoesNotExist:
                raise serializers.ValidationError("محصول موردنظر وجود ندارد.")

        if value > store_item.stock:
            raise serializers.ValidationError(f"موجودی کافی نیست. حداکثر موجودی برای این محصول: {store_item.stock}")

        return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'is_active', 'items', 'total_price']
        read_only_fields = ['id', 'user', 'total_price']