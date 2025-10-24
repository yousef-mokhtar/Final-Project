from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from products.models import Product
from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    - GET: لیست تمام نظرات برای یک محصول خاص را برمی‌گرداند.
    - POST: یک نظر جدید برای یک محصول ثبت می‌کند.
    """
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        product_id = self.kwargs.get('product_pk')
        return Review.objects.filter(product_id=product_id, is_approved=True)

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_pk')
        product = Product.objects.get(id=product_id)
        serializer.save(user=self.request.user, product=product)