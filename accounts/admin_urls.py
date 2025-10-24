from rest_framework.routers import DefaultRouter
from .views import UserAdminViewSet

router = DefaultRouter()
router.register(r'users', UserAdminViewSet, basename='admin-user')

urlpatterns = router.urls