from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Address

class AddressInline(admin.TabularInline):
    model = Address
    extra = 1 
    fields = ('title', 'province', 'city', 'postal_code', 'address_line', 'is_default')
    verbose_name = "آدرس"
    verbose_name_plural = "آدرس‌ها"

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [AddressInline] 

    list_display = ('email', 'username', 'phone', 'is_verified', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verified', 'groups')
    search_fields = ('email', 'username', 'phone', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'province', 'city', 'is_default')
    list_filter = ('province', 'city', 'is_default')
    search_fields = ('user__email', 'title', 'city', 'address_line')
    autocomplete_fields = ('user',) 