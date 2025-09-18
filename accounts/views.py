from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import User, Address
from .serializers import UserSerializer, AddressSerializer, OTPCodeSerilizer


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

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save()


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    