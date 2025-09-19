from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Cart.objects.get_or_create(user=self.request.user, is_active=True, is_deleted=False)[0]
        # cart, _ = Cart.objects.get_or_create(user=self.request.user, is_active=True, is_deleted=False)
        # return cart

