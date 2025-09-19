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

class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serilizer):
        from seller.models import StoreItem
        store_item = StoreItem.objects.get(id=self.kwargs['store_item_id'], is_deleted=False)
        cart = Cart.objects.get(user=self.request.user, is_active=True, is_deleted=False)
        serilizer.save(cart=cart, store_item=store_item)