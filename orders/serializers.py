from rest_framework import serializers
from .models import Order, OrderItem, Invoice, Payment

class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
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
   
    
class InvoiceSerializer(serializers.ModelSerializer):
    final_amount = serializers.ReadOnlyField()

    class Meta:
        model = Invoice
        fields = ['id', 'order', 'user', 'invoices_number', 'amount', 'tax', 'discount', 'status', 'issued_at', 'paid_at', 'final_amount']
        read_only_fields = ['id', 'order', 'user', 'invoices_number', 'amount', 'issued_at', 'paid_at', 'final_amount']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'orders', 'amount', 'status', 'paid_at', 'transaction_id', 'gateway_response']
        read_only_fields = ['id', 'orders', 'amount', 'paid_at', 'transaction_id', 'gateway_response']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('مبلغ پرداخت باید مثبت باشد.')
        return value

    def validate(self, data):
        order = data.get('orders')
        if order and order.is_paid:
            raise serializers.ValidationError('این سفارش قبلاً پرداخت شده است.')
        return data