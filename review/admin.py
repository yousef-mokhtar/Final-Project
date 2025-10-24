from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('user__email', 'product__name', 'text')
    autocomplete_fields = ('user', 'product')
    actions = ['approve_reviews', 'disapprove_reviews']

    @admin.action(description='تایید نظرات انتخاب شده')
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description='عدم تایید نظرات انتخاب شده')
    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)