from rest_framework.routers import DefaultRouter
from .views import AdminCategoryViewSet, AdminProductViewSet

router = DefaultRouter()
router.register(r'categories', AdminCategoryViewSet, basename='admin-category')
router.register(r'products', AdminProductViewSet, basename='admin-product')

urlpatterns = router.urls