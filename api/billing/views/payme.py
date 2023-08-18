import requests
from drf_spectacular.utils import extend_schema

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.billing.paginations import BillingPagination
from api.mixins import HandleExceptionMixin

from api.billing.serializers.payme import SubscribeSerializer, MerchantSerializer, PaymeGeneratePayLinkSerializer
from apps.billing.payme.models import PaymeTransaction, MerchantTransactionsModel
from apps.billing.models import UserPayment
from utils.swagger_tags import Payment
from utils.responses import Response as CustomResponse
from service.billing import PaymeService, PaymeMerchantService


class MerchantApiView(GenericAPIView):
    serializer_class = MerchantSerializer
    queryset = MerchantTransactionsModel.objects.all()
    permission_classes = ()
    authentication_classes = ()
    services = PaymeMerchantService()

    @extend_schema(tags=[Payment.Payme.PREFIX])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.services.call_back(request)

        return Response(data=result)


class PaymeGeneratePayLinkView(HandleExceptionMixin, GenericAPIView):
    serializer_class = PaymeGeneratePayLinkSerializer
    queryset = UserPayment.objects.filter(is_active=True)
    pagination_class = BillingPagination
    service = PaymeService()

    @extend_schema(tags=[Payment.Payme.PREFIX])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.service.generate_pay_link(order_id=serializer.validated_data['order_id'],
                                                amount=serializer.validated_data['amount'])
        return CustomResponse(data=result)


# class CardCreateApiView(HandleExceptionMixin, GenericAPIView):
class CardCreateApiView(GenericAPIView):
    serializer_class = SubscribeSerializer
    queryset = PaymeTransaction.objects.all()
    pagination_class = BillingPagination
    permission_classes = (IsAuthenticated,)
    service = PaymeService()

    @extend_schema(tags=[Payment.Payme.PREFIX])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = self.service.create_card(**serializer.validated_data)

        return Response(result)
