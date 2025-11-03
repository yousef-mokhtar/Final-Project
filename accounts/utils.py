import redis
from django.conf import settings
from django.core.cache import cache

# r = redis.Redis(
#     host=settings.REDIS_HOST,
#     port=settings.REDIS_PORT,
#     db=settings.REDIS_DB,
#     decode_responses=True # خروجی بجای بایت به شکل رشته
# )


def save_otp(username, otp):
    """Generate and store OTP code in Redis for 2 minutes"""
    cache.set(f"otp:{username}", otp, 120)
    return otp


def verify_otp(username, otp):
    """Verify the OTP stored in Redis"""
    stored = cache.get(f"otp:{username}")
    if stored and stored == otp:
        cache.delete(f"otp:{username}") 
        return True
    return False