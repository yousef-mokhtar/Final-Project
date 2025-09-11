from django.db import models
from core.models import BaseModel
from accounts.models import User

class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
