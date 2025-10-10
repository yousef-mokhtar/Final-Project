from django.contrib import admin
from .models import Category, Product, ProductImage

@admin.action(description='فعال کردن موارد انتخاب شده')
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description='غیرفعال کردن موارد انتخاب شده')
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    verbose_name = "تصویر محصول"
    verbose_name_plural = "گالری تصاویر"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active',)
    actions = [make_active, make_inactive]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'category', 'brand', 'is_active', 'created_at')
    list_filter = ('category', 'brand', 'is_active')
    search_fields = ('name', 'description', 'brand')
    ordering = ('-created_at',)
    actions = [make_active, make_inactive]
    autocomplete_fields = ('category',)  

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text')
    search_fields = ('product__name',)
    autocomplete_fields = ('product',)