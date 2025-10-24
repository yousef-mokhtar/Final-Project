# from django.urls import path
# from .views import CreateReviewView

# urlpatterns = [
#     path('products/<int:id>/review_create/', CreateReviewView.as_view(), name='review_create'),
# ]




from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet

router = DefaultRouter()
router.register(r'', ReviewViewSet, basename='review')

urlpatterns = router.urls