from django.test import TestCase
from celery import shared_task
from accounts.models import OTPCode, User
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_otp_code(user_id, code):
    user = User.objects.get(id=user_id)
    