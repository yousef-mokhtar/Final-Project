from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Order, OrderItem, Invoice
from .serializers import OrderSerializer, InvoiceSerializer
from cart.models import Cart


class MyOrderView(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_deleted=False)


class CheckoutView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart = Cart.objects.get(user=self.request.user, is_active=True, is_deleted=False)
        order = serializer.save(user=self.request.user)
        for item in cart.items.filter(is_deleted=False):
            OrderItem.objects.create(order=order,  store_item = item.store_item, quantity=item.quantity, price=item.store_item.price)
            order.calculate_total()
            Invoice.objects.create(order=order, user=self.request.user, invoices_number=f'INV-{order.id}', amount=order.total_price)
            cart.is_active = False
            cart.save()


class AdminOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(is_deleted=False)
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
