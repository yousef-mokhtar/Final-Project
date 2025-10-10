from django.urls import path
from .views import CreateReviewView

urlpatterns = [
    path('products/<int:id>/review_create/', CreateReviewView.as_view(), name='review_create'),
]