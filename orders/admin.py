from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'is_paid', 'paid_at', 'created_at')
    list_filter = ('status', 'is_paid')
    search_fields = ('user__email', 'id')
    
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'store_item', 'quantity', 'price', 'total_price')
    search_fields = ('order__id', 'store_item__name')