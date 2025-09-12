from django.contrib import admin
from .models import Store, StoreItem

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'is_active')
    search_fields = ('name', 'owner__email')
    
@admin.register(StoreItem)
class StoreItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'product', 'price', 'stock', 'created_at', 'is_active')
    list_filter = ('store', 'category')
    search_fields = ('name', 'product__name', 'store__name')