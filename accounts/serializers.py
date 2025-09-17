from rest_framework import serializers
from .models import User, Address, OTPCode
from rest_framework_simplejwt.serializers import TokenObtainSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'username', 'first_name', 'last_name']
        read_only_fields = ['id']

    email = serializers.EmailField(
        error_messages={"unique": "این ایمیل قبلاً ثبت شده است."}
    )

    phone = serializers.CharField(
        min_length=11,
        max_length=11,
        error_messages={
            "min_length": "شماره تلفن باید 11 رقمی باشد.",
            "max_length": "شماره تلفن باید 11 رقمی باشد.",
            "unique": "این شماره تلفن قبلاً ثبت شده است.",
        },
    )
