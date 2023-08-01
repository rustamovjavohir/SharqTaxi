from django.urls import path, include
from api.vehicle.routers import router

urlpatterns = [
    path('', include(router.urls)),
]
