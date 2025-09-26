from celery import shared_task
from django.core.mail import send_mail
from accounts.models import User

@shared_task
def send_otp_code(user_id, code):
    try:
        user = User.objects.get(id=user_id)
        send_mail(
            'کد OTP شما',
            f'کد تأیید شما: {code}',
            'from@test.com',
            [user.email],
            fail_silently=False,
        )
    except User.DoesNotExist:
        pass  # لاگ خطا یا مدیریت خطا