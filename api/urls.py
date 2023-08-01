from django.urls import path, include

from api.auth_user.urls import (auth_jwt_urlpatterns as auth_jwt_urls,
                                user_urlpatterns as user_urls,
                                auth_token_urlpatterns as token_urls,
                                router as auth_user_router)
from api.vehicle.urls import urlpatterns as vehicle_urls
from api.billing.urls import urlpatterns as billing_urls
from api.oauth2.urls import urlpatterns as oauth2_urls

urlpatterns = [
    path('jwt/', include(auth_jwt_urls)),
    path('token/', include(token_urls)),
    path('user/', include(user_urls)),
    path('vehicle/', include(vehicle_urls)),
    path('billing/', include(billing_urls)),
    path('oauth2/', include(oauth2_urls)),
]
