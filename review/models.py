from django.db import models
from core.models import BaseModel
from accounts.models import User
from products.models import Product

class Review(BaseModel):
    class Rating(models.IntegerChoices):
        ONE = 1, "1"
        TWO = 2, "2"
        THREE = 3, "3"
        FOUR = 4, "4"
        FIVE = 5, "5"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(choices=Rating.choices)
    text = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "product")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.rating}⭐)"