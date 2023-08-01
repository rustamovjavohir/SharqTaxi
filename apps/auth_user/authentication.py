from django.utils.translation import gettext_lazy as _

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.auth_user.models import Token


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        token = Token.objects.select_related('user').filter(key=key).first()

        if token is None:
            raise AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise AuthenticationFailed(_('User inactive or deleted.'))

        return token.user, token
