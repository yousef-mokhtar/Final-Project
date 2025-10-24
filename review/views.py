from django.shortcuts import render
from rest_framework import generics 
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from .models import Review
from .serializers import ReviewSerializer

class CreateReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs['id']
        product = Product.objects.get(id=product_id, is_deleted=False)
        serializer.save(user=self.request.user, product=product)