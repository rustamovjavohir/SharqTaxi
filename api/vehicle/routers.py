from rest_framework.routers import DefaultRouter
from api.vehicle.views import car

router = DefaultRouter()

router.register('car', car.CarViewSet, basename='car')
