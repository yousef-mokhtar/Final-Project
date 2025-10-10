from django.contrib import admin
from .models import Order, OrderItem, Invoice, Payment

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('store_item', 'quantity', 'price')
    autocomplete_fields = ('store_item',)
    verbose_name = "آیتم سفارش"
    verbose_name_plural = "آیتم‌های سفارش"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'user', 'status', 'is_paid', 'total_price', 'created_at')
    list_filter = ('status', 'is_paid', 'created_at')
    search_fields = ('id', 'user__email')
    ordering = ('-created_at',)
    autocomplete_fields = ('user', 'shipping_address')
    actions = ['set_status_to_processing', 'set_status_to_completed', 'set_status_to_canceled']

    @admin.action(description="تغییر وضعیت به 'در حال پردازش'")
    def set_status_to_processing(self, request, queryset):
        queryset.update(status=Order.Status.PROCESSING)

    @admin.action(description="تغییر وضعیت به 'تکمیل شده'")
    def set_status_to_completed(self, request, queryset):
        queryset.update(status=Order.Status.COMPLETED)

    @admin.action(description="تغییر وضعیت به 'لغو شده'")
    def set_status_to_canceled(self, request, queryset):
        queryset.update(status=Order.Status.CANCELED)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'store_item', 'quantity', 'price')
    autocomplete_fields = ('order', 'store_item')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'invoices_number', 'amount', 'status')
    list_filter = ('status',)
    search_fields = ('invoices_number', 'user__email')
    autocomplete_fields = ('order', 'user')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('orders', 'amount', 'status', 'paid_at', 'transaction_id')
    list_filter = ('status',)
    search_fields = ('transaction_id', 'orders__id')
    autocomplete_fields = ('orders',)