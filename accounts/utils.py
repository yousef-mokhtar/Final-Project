import redis
from django.conf import settings
from django.core.cache import cache

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True # خروجی بجای بایت به شکل رشته
)


def save_otp(phone, otp):
    """Generate and store OTP code in Redis for 2 minutes"""
    cache.set(f"otp:{phone}", otp, 120)
    return otp


def verify_otp(phone, otp):
    """Verify the OTP stored in Redis"""
    stored = r.get(f"otp:{phone}")
    if stored and stored == otp:
        r.delete(f"otp:{phone}") 
        return True
    return False