from django.db import models
from core.models import BaseModel
from accounts.models import User
from products.models import Category


class Store(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, )
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.TextField()

class StoreItem(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10)
    stock = models.PositiveIntegerField()
    