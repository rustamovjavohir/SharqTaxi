from api.billing.paginations import BillingPagination
from api.billing.serializers.card import BankCardSerializer, BankCardSerializer, BankCardUpdateSerializer
from api.billing.serializers.promotion import PromotionSerializer
from api.billing.serializers.payment import UserPaymentSerializer
from rest_framework.viewsets import ModelViewSet
from api.mixins import ActionSerializerMixin, ActionPermissionMixin, ReturnResponseMixin
from apps.auth_user.permissions import IsOwnerClientCard
from apps.billing.models import UserPayment, BankCard, Promotion
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.swagger_tags import Mobile
from drf_spectacular.utils import extend_schema
from apps.billing import cosntants


class UserPaymentViewSet(ActionSerializerMixin, ActionPermissionMixin, ReturnResponseMixin, ModelViewSet):
    queryset = UserPayment.objects.filter(is_active=True)
    serializer_class = UserPaymentSerializer
    pagination_class = BillingPagination
    ACTION_SERIALIZERS = {
        'list': UserPaymentSerializer,
        'retrieve': UserPaymentSerializer,
        'create': UserPaymentSerializer,
        'update': UserPaymentSerializer,
        'partial_update': UserPaymentSerializer,
    }
    ACTION_PERMISSIONS = {
        'list': [AllowAny, ],
        'retrieve': [IsAuthenticated],
        'create': [IsAuthenticated],
        'update': [IsAuthenticated],
        'partial_update': [IsAuthenticated],
    }

    @extend_schema(tags=[Mobile.Client.PAYMENT])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Client.PAYMENT])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Client.PAYMENT])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Client.PAYMENT])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Client.PAYMENT])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Client.PAYMENT])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class BankCardViewSet(ActionSerializerMixin, ActionPermissionMixin, ReturnResponseMixin, ModelViewSet):
    queryset = BankCard.objects.filter(is_active=True)
    serializer_class = BankCardSerializer
    pagination_class = BillingPagination
    ACTION_SERIALIZERS = {
        'list': BankCardSerializer,
        'retrieve': BankCardSerializer,
        'update': BankCardUpdateSerializer,
    }
    ACTION_PERMISSIONS = {
        'list': [IsAuthenticated, ],
        'retrieve': [IsAuthenticated],  # TODO switch to  IsOwnerClientCard
        'create': [IsAuthenticated],
        'update': [IsAuthenticated],
        'destroy': [IsOwnerClientCard],
    }

    @extend_schema(tags=[Mobile.Client.CARD])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Client.CARD])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Client.CARD])
    def create(self, request, *args, **kwargs):
        return super().create(request, message=cosntants.BANK_CARD_SUCCESSFULLY_CREATED, *args, **kwargs)

    @extend_schema(tags=[Mobile.Client.CARD])
    def update(self, request, *args, **kwargs):
        return super().update(request, message=cosntants.BANK_CARD_SUCCESSFULLY_UPDATED, *args, **kwargs)

    @extend_schema(tags=[Mobile.Client.CARD])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Client.CARD])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, message=cosntants.BANK_CARD_SUCCESSFULLY_DELETED, *args, **kwargs)
