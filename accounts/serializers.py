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

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
            model = Address
            fields = ['id', 'title', 'province', 'city', 'postal_code', 'address_line', 'is_default']
            read_only_fields = ['id', 'user']  # کاربر خودش یوزر رو ست نکنه
    
    def validate(self, attrs):
        user = self.context['request'].user
        if attrs.get('is_default'):
            Address.objects.filter(user=user, is_default=True).update(is_default=False) # خاموش کردن آدرس های پیش فرض قبلی
        return attrs
    
class OTPCodeRequestSerilizer(serializers.Serializer):
    # class Meta:
    #     model = OTPCode

    # اینجا این باید تکمیل بشه 
    email = serializers.CharField(max_length=25)

class OTPCodeVerifySerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=6,
        min_length=6,
        error_messages={
             "min_length": "کد OTP باید 6 رقمی باشد.",
             "max_length": "کد OTP باید 6 رقمی باشد.",
        },
    )
    phone = serializers.CharField(
        max_length=11,
        min_length=11,
        error_messages={
            "min_length": "شماره تلفن باید 11 رقمی باشد.",
            "max_length": "شماره تلفن باید 11 رقمی باشد.",
        },
    )