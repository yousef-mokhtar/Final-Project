from datetime import timedelta, timezone
import random
from django.shortcuts import render, get_object_or_404 
from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.tasks import send_otp_code
from .models import User, Address
from .serializers import UserSerializer, AddressSerializer, OTPCodeRequestSerializer, OTPCodeVerifySerializer, CustomTokenObtainPairSerializer
from .utils import save_otp, verify_otp
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_verified=False)  # کاربر ثبت می‌شه ولی تأیید نشده
        return Response({
            'message': f'کاربر با موفقیت ثبت شد. لطفاً کد OTP را از طریق /api/accounts/otp/request/ درخواست کنید.',
            'user_id': user.id,
            'email': user.email,
            'phone': user.phone
        }, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class TokenRefresh(TokenRefreshView):
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

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class OTPRequestView(generics.GenericAPIView):
    serializer_class = OTPCodeRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']

        user = get_object_or_404(User, username=username)
        email = user.email 

        if not email:
            return Response(
                {'error': 'کاربر ایمیل ثبت شده‌ای ندارد.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        code = str(random.randint(100000, 999999))
        save_otp(username=username, otp=code)

        send_otp_code.delay(user.id, code)

        return Response({'message': f'کد OTP به ایمیل {email} ارسال شد.'}, status=status.HTTP_200_OK)


class OTPVerifyView(generics.GenericAPIView):
    serializer_class = OTPCodeVerifySerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Verify OTP code",
        description="Verifies the OTP code sent via email and marks the user as verified."
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        code = serializer.validated_data['code']

        user = get_object_or_404(User, username=username, is_deleted=False)
        # email = user.email

        if verify_otp(username=username, otp=code):
            try:
                # user = User.objects.get(email=email, is_deleted=False)
                user.is_verified = True
                user.save()
                return Response(
                    {'message': 'حساب کاربری شما با موفقیت تأیید شد.'},
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response(
                    {'error': 'کاربری با این ایمیل یافت نشد.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {'error': 'کد OTP نامعتبر یا منقضی شده است.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class UserAdminViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای مدیریت کامل (CRUD) کاربران توسط ادمین.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]