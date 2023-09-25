from django.urls import path, include

from api.auth_user.views.authorization import (LoginView, GetRefreshTokenView, CustomTokenVerifyView, LogoutView, \
                                               LoginTokenView, LogOutTokenView, VerifyTokenView, CaptchaApiView)
from api.auth_user.views.user import (ProfileUserView, ChangePasswordView, ResetPasswordView)
from api.auth_user.routers import router

auth_jwt_urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', GetRefreshTokenView.as_view(), name='refresh'),
    path('verify/', CustomTokenVerifyView.as_view(), name='verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

auth_token_urlpatterns = [
    path('login/', LoginTokenView.as_view(), name='token-login'),
    path('logout/', LogOutTokenView.as_view(), name='token-logout'),
    path('captcha/', CaptchaApiView.as_view(), name='captcha'),
]

user_urlpatterns = [
    path('profile/', ProfileUserView.as_view(), name='profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('reset_password/', ResetPasswordView.as_view(), name='password-reset'),
    path('verify/', VerifyTokenView.as_view(), name='token-verify'),
    path('', include(router.urls)),
]
