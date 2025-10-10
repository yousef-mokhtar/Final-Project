from django.db import models
from core.models import BaseModel
from accounts.models import User
from products.models import Category, Product

class Store(BaseModel):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='store')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class StoreAddress(BaseModel):
    """ آدرس‌های مرتبط با یک فروشگاه """
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='addresses')
    title = models.CharField(max_length=50)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    address_line = models.TextField()
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.store.name} - {self.title}"

class StoreItem(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) 
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} in {self.store.name}"