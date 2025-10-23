from celery import shared_task
from django.core.mail import send_mail
from .models import Order
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_payment_success_email(order_id):
    """
    یک تسک Celery برای ارسال ایمیل به کاربر پس از پرداخت موفق.
    """
    try:
        order = Order.objects.get(id=order_id)
        user = order.user
        send_mail(
            subject=f'پرداخت سفارش #{order.id} شما با موفقیت انجام شد',
            message=f'سلام {user.username} عزیز،\n\nپرداخت سفارش شما به مبلغ {order.total_price} تومان با موفقیت ثبت شد. سفارش شما در حال پردازش است.\n\nسپاس از خرید شما!\nتیم کاستومی',
            from_email='noreply@customie.com',
            recipient_list=[user.email],
            fail_silently=False,
        )
        logger.info(f"Payment success email sent for order ID: {order_id}")
    except Order.DoesNotExist:
        logger.error(f"Order with id {order_id} not found for sending email.")
    except Exception as e:
        logger.error(f"Failed to send payment email for order {order_id}: {str(e)}")