from django.db import models
from core.models import BaseModel
from orders.models import Order

class Payment(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"
    
    orders = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=15, decimal_places=0)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    paid_at = models.DateField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    