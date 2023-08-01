from api.auth_user.views import user
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('driver', user.UserDriverViewSet, basename='driver')
router.register('client', user.UserClientViewSet, basename='client')
