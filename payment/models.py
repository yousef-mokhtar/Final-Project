from django.db import models
from core.models import BaseModel
from accounts.models import User
from seller.models import StoreItem

class Cart(BaseModel):
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name='cart')
    is_active = models.BooleanField(default=True)
    def total_price(self):
        return sum([item.total_price for item in self.items.all()])
    
class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    store_item = models.ForeignKey(StoreItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
