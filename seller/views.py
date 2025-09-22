from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Store, StoreItem
from serializers import StoreSerializer, StoreItemSerializer

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
    serializer_class = StoreItem
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StoreItem.objects.filter(store__owner=self.request.user, is_deleted=False)
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()