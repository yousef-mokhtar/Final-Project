from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.shortcuts import redirect
from django.conf import settings
from django.utils import timezone
from .models import Order, OrderItem, Invoice, Payment
from .serializers import OrderSerializer, InvoiceSerializer, PaymentSerializer
from cart.models import Cart
import requests

MERCHANT_ID = settings.ZARINPAL_MERCHANT_ID
ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"  # sandbox
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/"
CALLBACK_URL = "http://127.0.0.1:8000/api/orders/verify/"

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
            OrderItem.objects.create(order=order, store_item=item.store_item, quantity=item.quantity, price=item.store_item.price)
        order.calculate_total()
        Invoice.objects.create(order=order, user=self.request.user, invoices_number=f'INV-{order.id}', amount=order.total_price)
        
        payment = Payment.objects.create(orders=order, amount=order.total_price)
        
        data = {
            "merchant_id": MERCHANT_ID,
            "amount": int(order.total_price),
            "callback_url": CALLBACK_URL,
            "description": f"پرداخت سفارش #{order.id}",
        }
        headers = {"accept": "application/json", "content-type": "application/json"}
        res = requests.post(ZP_API_REQUEST, json=data, headers=headers)
        res_json = res.json()
        if res_json.get('data', {}).get('code') == 100:
            authority = res_json['data']['authority']
            payment.transaction_id = authority
            payment.gateway_response = res_json
            payment.save()
            cart.is_active = False
            cart.save()
            return Response({"payment_url": ZP_API_STARTPAY + authority}, status=status.HTTP_200_OK)
        else:
            return Response({"error": res_json.get('errors')}, status=status.HTTP_400_BAD_REQUEST)
        

class VerifyPaymentView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        authority = request.GET.get("Authority")
        status = request.GET.get("Status")
        payment = Payment.objects.get(transaction_id=authority)
        order = payment.orders
        amount = int(payment.amount)
        if status == "OK":
            data = {
                "merchant_id": MERCHANT_ID,
                "amount": amount,
                "authority": authority,
            }
            headers = {"accept": "application/json", "content-type": "application/json"}
            res = requests.post(ZP_API_VERIFY, json=data, headers=headers)
            res_json = res.json()
            if res_json.get('data', {}).get('code') == 100:
                payment.status = Payment.Status.SUCCESS
                payment.paid_at = timezone.now()
                payment.gateway_response = res_json
                payment.save()
                order.is_paid = True
                order.status = Order.Status.PROCESSING
                order.paid_at = timezone.now()
                order.save()
                return Response({"status": "success", "ref_id": res_json["data"]["ref_id"]})
            else:
                payment.status = Payment.Status.FAILED
                payment.gateway_response = res_json
                payment.save()
                return Response({"error": res_json["data"]["message"]})
        else:
            payment.status = Payment.Status.FAILED
            payment.save()
            return Response({"status": "canceled"})

class AdminOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(is_deleted=False)
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(orders__user=self.request.user, is_deleted=False)

    def perform_create(self, serializer):
        order_id = self.request.data.get('order_id')
        order = Order.objects.get(id=order_id, user=self.request.user, is_paid=False)
        payment = serializer.save(orders=order, amount=order.total_price)
        return payment

class StartPaymentView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        payment_id = kwargs.get('pk')  
        payment = Payment.objects.get(id=payment_id, orders__user=request.user, orders__is_paid=False)
        order = payment.orders
        amount = int(order.total_price)
        description = f"پرداخت سفارش #{order.id}"
        data = {
            "merchant_id": MERCHANT_ID,
            "amount": amount,
            "callback_url": CALLBACK_URL,
            "description": description,
        }
        headers = {"accept": "application/json", "content-type": "application/json"}
        res = requests.post(ZP_API_REQUEST, json=data, headers=headers)
        res_json = res.json()
        if res_json.get('data', {}).get('code') == 100:
            authority = res_json['data']['authority']
            payment.transaction_id = authority
            payment.gateway_response = res_json
            payment.save()
            return Response({"payment_url": ZP_API_STARTPAY + authority})
        else:
            return Response({"error": res_json.get('errors')}, status=status.HTTP_400_BAD_REQUEST)