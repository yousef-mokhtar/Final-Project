from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
            model = Payment
            fields = ['id', 'orders', 'amount', 'status', 'paid_at', 'transaction_id']
            read_only_fields = ['id', 'orders', 'amount', 'paid_at', 'transaction_id']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('مبلغ پرداخت باید مثبت باشد.')
        return value
    
    def validate(self, data):
        order = data.get('orders')
        if order and order.is_paid: # گذاشتن اوردر برای رفع AttributeError
            raise serializers.ValidationError('این سفارش قبلاً پرداخت شده است.')
        return data
    