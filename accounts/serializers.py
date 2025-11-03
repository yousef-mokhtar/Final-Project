from rest_framework import serializers
from .models import User, Address
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    email = serializers.EmailField(
        required=True,
        error_messages={"unique": "این ایمیل قبلاً ثبت شده است."}
    )

    class Meta:
        model = User
        fields = ['email', 'phone', 'username', 'first_name', 'last_name', 'password'] 
        # read_only_fields = ['id']


    phone = serializers.CharField(
        min_length=11,
        max_length=11,
        error_messages={
            "min_length": "شماره تلفن باید 11 رقمی باشد.",
            "max_length": "شماره تلفن باید 11 رقمی باشد.",
            "unique": "این شماره تلفن قبلاً ثبت شده است.",
        },
    )

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_verified = False 
        user.save()
        return user

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'title', 'province', 'city', 'postal_code', 'address_line', 'is_default']
        read_only_fields = ['id', 'user']
    
    def validate(self, attrs):
        user = self.context['request'].user
        if attrs.get('is_default'):
            Address.objects.filter(user=user, is_default=True).update(is_default=False)
        return attrs

class OTPCodeRequestSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)   

class OTPCodeVerifySerializer(serializers.Serializer):

    code = serializers.CharField(
        max_length=6,
        min_length=6,
        error_messages={
             "min_length": "کد OTP باید 6 رقمی باشد.",
             "max_length": "کد OTP باید 6 رقمی باشد.",
        },
    )
    username = serializers.CharField(max_length=150)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        attrs['username'] = attrs.get('email')
        return super().validate(attrs)