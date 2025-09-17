from rest_framework import serializers
from .models import Order, OrderItem, Invoice

class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()

    class Meta:
        mdoel = OrderItem
        fields = ['id', 'store_item', 'quantity', 'price', 'total_price']
        read_only_fields = ['id', 'price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'shipping_address', 'total_price', 'status', 'is_paid', 'paid_at', 'items']
        read_only_fields = ['id', 'user', 'total_price', 'is_paid', 'paid_at']

    def validate(self, data):
        if not data.get('shipping_address'):
            raise serializers.ValidationError('آدرس ارسال الزامی است.')
        return data