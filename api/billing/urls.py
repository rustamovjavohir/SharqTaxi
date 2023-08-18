from django.urls import path, include

from api.billing.routers import router
from api.billing.urls_payme import urlpatterns as payme_urls

urlpatterns = [
    path('', include(router.urls)),
    path('payme/', include(payme_urls)),
]
