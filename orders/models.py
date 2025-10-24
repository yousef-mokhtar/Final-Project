from django.db import models
from core.models import BaseModel
from accounts.models import Address, User
from products.models import Product
from seller.models import StoreItem

class Order(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        COMPLETED = "completed", "Completed"
        CANCELED = "canceled", "Canceled"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    is_paid = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)

    def calculate_total(self):
        self.total_price = sum([item.total_price for item in self.items.all()])
        self.save()

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    store_item = models.ForeignKey(StoreItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=0)

    class Meta:
        unique_together = ('order', 'store_item')

    @property
    def total_price(self):
        return self.quantity * self.price

class Invoice(BaseModel):
    class Status(models.TextChoices):
        UNPAID = "unpaid", "Unpaid"
        PAID = "paid", "Paid"
        CANCELED = "canceled", "Canceled"
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    invoices_number = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=15, decimal_places=0)
    tax = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    discount = models.DecimalField(max_digits=15, decimal_places=0,default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNPAID)
    issued_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Invoice {self.invoices_number} - {self.user.email}'
    
    def final_amount(self):
        self.amount = self.order.total_price + self.tax - self.discount
        return self.amount

class Payment(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"
    
    orders = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=15, decimal_places=0)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    gateway_response = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f'Payment for Order #{self.orders.id} - {self.status}'