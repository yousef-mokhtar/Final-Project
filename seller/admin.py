from django.contrib import admin
from .models import Store, StoreItem

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'is_active')
    search_fields = ('name', 'owner__email')
    
admin.site.register(StoreItem)