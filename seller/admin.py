from django.contrib import admin
from .models import Store, StoreItem

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__email')

@admin.register(StoreItem)
class StoreItemAdmin(admin.ModelAdmin):
    list_display = ('store', 'product', 'price', 'stock')
    list_filter = ('store', 'product')
    search_fields = ('store__name', 'product__name')