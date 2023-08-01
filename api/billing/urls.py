from django.urls import path, include

from api.billing.routers import router

urlpatterns = [
    path('', include(router.urls)),
]
