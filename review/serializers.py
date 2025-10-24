from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'text', 'is_approved']
        read_only_fields = ['id', 'user', 'is_approved']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("امتیاز باید بین 1 تا 5 باشد.")
        return value
    
    def validate(self, data):
            user = self.context['request'].user
            product = data.get('product')
            if Review.objects.filter(user=user, product=product).exists():
                raise serializers.ValidationError("شما قبلاً برای این محصول نظر ثبت کرده‌اید.")
            return data