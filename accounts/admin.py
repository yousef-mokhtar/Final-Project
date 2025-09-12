from django.contrib import admin
from .models import User, Address, OTPCode
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'phone', 'is_verified', 'is_staff', 'is_active')
    list_filter = ('is_verified', 'is_staff', 'is_active', 'groups')
    search_fields = ('email', 'username', 'phone')
    ordering = ('email',)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'province', 'city', 'postal_code', 'is_default')
    list_filter = ('province', 'city', 'is_default')
    search_fields = ('user__email', 'title', 'city', 'province', 'postal_code')

@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'expiration_time', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('user__email', 'code')
