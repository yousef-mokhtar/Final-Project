from rest_framework import serializers
from .models import User, Address, OTPCode
from rest_framework_simplejwt.serializers import TokenObtainSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta: