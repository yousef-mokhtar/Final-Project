from django.db import models
from core.models import BaseModel
from accounts.models import User

class Store(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, )
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.TextField()
    