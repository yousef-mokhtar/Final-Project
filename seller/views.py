from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Store, StoreItem
from .serializers import StoreAddressSerializer, StoreSerializer, StoreItemSerializer
from rest_framework.exceptions import PermissionDenied
from orders.models import OrderItem
from orders.serializers import OrderItemSerializer 

class RegisterAsSellerView(generics.CreateAPIView):
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MyStoreView(generics.RetrieveUpdateAPIView):
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Store.objects.get(owner=self.request.user, is_deleted=False)
    

class StoreItemViewSet(viewsets.ModelViewSet):
    serializer_class = StoreItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StoreItem.objects.filter(store__owner=self.request.user, is_deleted=False)
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class StoreAddressViewSet(viewsets.ModelViewSet):
    serializer_class = StoreAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_store_instance(self):
        try:
            return Store.objects.get(owner=self.request.user)
        except Store.DoesNotExist:
            raise PermissionDenied("You do not own a store.")

    def get_queryset(self):
        store = self.get_store_instance()
        return store.addresses.filter(is_deleted=False)

    def perform_create(self, serializer):
        store = self.get_store_instance()
        serializer.save(store=store)

class StoreOrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset برای نمایش آیتم‌های سفارشی که مربوط به فروشگاه کاربر لاگین کرده است.
    """
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'store'):
            return OrderItem.objects.none() 
        
        return OrderItem.objects.filter(store_item__store=user.store).order_by('-created_at')