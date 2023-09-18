from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.auth_user.paginations import UserPagination
from api.auth_user.serializers.authorization import (ChangeUserPasswordSerializer, ResetPasswordSerializer)
from apps.auth_user import constants
from repository.auth_user import UserRepository
from service.notifications import EmailService
from utils.responses import Response
from rest_framework.viewsets import ModelViewSet

from apps.auth_user.models import User, UserRole, UserDriver, UserClient
from rest_framework.generics import GenericAPIView
from api.auth_user.serializers.user import UserSerializer, UserDriverSerializer, UserDriverUpdateSerializer, \
    UserClientSerializer, UserClientUpdateSerializer, UserClientRetailSerializer
from utils.swagger_tags import Mobile
from utils.utils import get_json_data
from api.mixins import ActionPermissionMixin, ActionSerializerMixin, ReturnResponseMixin, HandleExceptionMixin


class ProfileUserView(HandleExceptionMixin, GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    @extend_schema(tags=[Mobile.Staff.PREFIX])
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @extend_schema(tags=[Mobile.Staff.PREFIX])
    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class ChangePasswordView(HandleExceptionMixin, GenericAPIView):
    serializer_class = ChangeUserPasswordSerializer
    permission_classes = [IsAuthenticated, ]

    @extend_schema(tags=[Mobile.Staff.PREFIX])
    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(message=serializer.data.get('message'), status=status.HTTP_200_OK)


class ResetPasswordView(HandleExceptionMixin, GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny, ]
    service = EmailService()
    user_service = UserRepository()

    @extend_schema(tags=[Mobile.Staff.PREFIX])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.user_service.get_user_by_email(serializer.data.get('email'))
        self.service.send_email(user, **serializer.data)
        return Response(message=constants.MESSAGE_SUCCESSFULLY_SENT, status=status.HTTP_200_OK)


class UserDriverViewSet(ActionSerializerMixin, ActionPermissionMixin, ReturnResponseMixin, ModelViewSet):
    queryset = UserDriver.objects.filter(user__is_active=True).order_by('-id')
    serializer_class = UserDriverSerializer
    pagination_class = UserPagination
    ACTION_SERIALIZERS = {
        'list': UserDriverSerializer,
        'retrieve': UserDriverSerializer,
        'update': UserClientUpdateSerializer,
        'partial_update': UserClientUpdateSerializer,
        'create': UserDriverSerializer,
    }
    ACTION_PERMISSIONS = {
        'list': [IsAuthenticated],
        'create': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'destroy': [IsAuthenticated],
        'update': [IsAuthenticated],
        'partial_update': [IsAuthenticated],
    }

    @extend_schema(tags=[Mobile.Driver.PREFIX])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Driver.PREFIX])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Driver.PREFIX])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Driver.PREFIX])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Driver.PREFIX])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Driver.PREFIX])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class UserClientViewSet(ActionSerializerMixin, ActionPermissionMixin, ReturnResponseMixin, ModelViewSet):
    queryset = UserClient.objects.filter(user__is_active=True).order_by('-id')
    serializer_class = UserClientSerializer
    pagination_class = UserPagination
    ACTION_SERIALIZERS = {
        'list': UserClientSerializer,
        'retrieve': UserClientRetailSerializer,
        'update': UserClientUpdateSerializer,
    }
    ACTION_PERMISSIONS = {
        'list': [IsAuthenticated],
        'update': [AllowAny, ],
        'partial_update': [AllowAny, ],
        'create': [AllowAny, ],
        'retrieve': [AllowAny, ],
        'destroy': [AllowAny, ],
    }

    @extend_schema(tags=[Mobile.Client.PREFIX])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Client.PREFIX])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Client.PREFIX])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Client.PREFIX])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Client.PREFIX])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Client.PREFIX])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
