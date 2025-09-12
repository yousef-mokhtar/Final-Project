from django.db import models
from core.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)


    def __str__(self):
        return self.name
    
