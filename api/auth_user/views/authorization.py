import base64
from io import BytesIO

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.mixins import HandleExceptionMixin
from apps.notifications.models import Token
from service.auth_user import UserServices
from service.notifications import EmailService
from utils.decorators import calculate_time
from utils.generates import generate_password
from utils.responses import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_spectacular.utils import extend_schema
from api.auth_user.serializers.authorization import (CustomObtainPairSerializer, CustomTokenRefreshSerializer,
                                                     CustomTokenVerifySerializer, LogoutSerializer,
                                                     TokenLoginSerializer, TokenLogOutSerializer, CaptchaSerializer,
                                                     )
from apps.auth_user import constants
from utils.swagger_tags import Mobile


class LoginView(TokenObtainPairView):
    serializer_class = CustomObtainPairSerializer

    @extend_schema(tags=[Mobile.Driver.AUTHORIZATION])
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response(data=response.data, message=constants.USER_LOG_IN, status=status.HTTP_200_OK)

    def handle_exception(self, exc):
        if getattr(exc, 'detail', None):
            return Response(error=exc.detail, success=False, status=exc.status_code)
        return Response(error=str(exc), success=False, status=exc.status_code)


class GetRefreshTokenView(HandleExceptionMixin, TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

    @extend_schema(tags=[Mobile.Driver.AUTHORIZATION])
    def post(self, request, *args, **kwargs):
        response = super(GetRefreshTokenView, self).post(request, *args, **kwargs)
        return Response(data=response.data, message=constants.TOKEN_REFRESHED, status=status.HTTP_200_OK)


class CustomTokenVerifyView(HandleExceptionMixin, TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer

    @extend_schema(tags=[Mobile.Driver.AUTHORIZATION])
    def post(self, request, *args, **kwargs):
        response = super(CustomTokenVerifyView, self).post(request, *args, **kwargs)
        return Response(data=response.data, message=constants.TOKEN_IS_VALID, status=status.HTTP_200_OK)


class LogoutView(HandleExceptionMixin, GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated, ]

    @extend_schema(tags=[Mobile.Driver.AUTHORIZATION])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.add_blacklist()
        return Response(message=constants.USER_LOG_OUT, status=status.HTTP_205_RESET_CONTENT)


class LoginTokenView(HandleExceptionMixin, GenericAPIView):
    serializer_class = TokenLoginSerializer

    @extend_schema(tags=[Mobile.Driver.AUTHORIZATION])
    @calculate_time
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, message=constants.USER_LOG_IN, status=status.HTTP_200_OK)


class LogOutTokenView(HandleExceptionMixin, GenericAPIView):
    serializer_class = TokenLogOutSerializer
    permission_classes = [IsAuthenticated, ]

    @extend_schema(tags=[Mobile.Driver.AUTHORIZATION])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(message=constants.USER_LOG_OUT, status=status.HTTP_205_RESET_CONTENT)


class VerifyTokenView(HandleExceptionMixin, APIView):
    permission_classes = [AllowAny, ]
    services = EmailService()
    user_services = UserServices()

    @extend_schema(tags=[Mobile.Staff.PREFIX])
    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        _token = Token.objects.filter(token=token, is_active=True).first()
        if _token:
            password = generate_password()
            self.services.deactivate_token(_token)
            self.user_services.set_user_password(_token.user, password)
            return Response(data={'new_password': password}, message=constants.TOKEN_IS_VALID,
                            status=status.HTTP_200_OK)
        return Response(message=constants.TOKEN_IS_INVALID_OR_EXPIRED,
                        success=False, status=status.HTTP_400_BAD_REQUEST)


class CaptchaApiView(HandleExceptionMixin, GenericAPIView):
    serializer_class = CaptchaSerializer
    permission_classes = [AllowAny, ]
    services = UserServices()

    @extend_schema(tags=[Mobile.Driver.AUTHORIZATION])
    def get(self, request, *args, **kwargs):
        byte = BytesIO()
        captcha = self.services.generate_captcha()
        captcha.save(byte, format=captcha.format)
        byte = byte.getvalue()
        data = {
            'captcha': base64.b64encode(byte),
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @extend_schema(tags=[Mobile.Driver.AUTHORIZATION])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        captcha = serializer.validated_data.get('captcha')
        if not self.services.verify_captcha(captcha):
            raise ValidationError(constants.CAPTCHA_IS_INVALID)
        return Response(data=True, message=constants.CAPTCHA_IS_VALID, status=status.HTTP_200_OK)
