# accounts/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from accounts.models import User
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_otp_code(user_id, code, recipient_email=None):
    try:
        user = User.objects.get(id=user_id)
        recipient = recipient_email or user.email
        send_mail(
            subject='کد OTP شما',
            message=f'سلام {user.username}، کد تأیید شما: {code}',
            from_email='from@test.com',
            recipient_list=[recipient],
            fail_silently=False,
        )
        logger.info(f"OTP {code} sent to {recipient}")
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} not found")
    except Exception as e:
        logger.error(f"Failed to send OTP to {recipient_email or 'unknown'}: {str(e)}")