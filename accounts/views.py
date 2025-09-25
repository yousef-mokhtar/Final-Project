from datetime import timedelta, timezone
import random
from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.tasks import send_otp_code
from .models import OTPCode, User, Address
from .serializers import UserSerializer, AddressSerializer, OTPCodeRequestSerilizer, OTPCodeVerifySerializer
from .utils import save_otp, verify_otp


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginView(TokenObtainPairView):
    pass


class TokenRefresh(TokenRefreshView):
    pass

class OTPRequestView(generics.GenericAPIView):
    pass


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    # Soft delete
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save()


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user, is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Soft delete
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class OTPRequestView(generics.GenericAPIView):
    serializer_class = OTPCodeSerilizer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        code = str(random.randint(100000, 999999))
        # expiration_time = timezone.now() + timedelta(minutes=5)
        save_otp(phone=user.phone, otp=code)
        # otp = OTPCode.objects.create(user=user, code=code, expiration_time=expiration_time)

        send_otp_code.delay(user.id, code)
        return Response({'message': 'کد OTP ارسال شد.'}, status=status.HTTP_200_OK)


class OTPVerifyView(generics.GenericAPIView):

    # خواندن اوتیپی و شماره تلفن از کاربر
    # خواندن اوتیپی از دیتابیس
    # مچ کردن این دو
    # اگر این دو باهم مچ بودن ثبت نام انجام میشه برای این کاربر
    # اگر مچ نبود ارور بده 

    serializer_class = OTPCodeVerifySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # دریافت داده‌ها از درخواست
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phone_number = serializer.validated_data['phone_number']
        otp_code = serializer.validated_data['otp_code']
        if verify_otp(phone=phone_number,otp=otp_code):
            request.user.is_verified = True