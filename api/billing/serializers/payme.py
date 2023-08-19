from uuid import UUID

from rest_framework import serializers

from apps.billing.payme.config import PAYME_MIN_AMOUNT
from apps.billing.payme.exceptions import IncorrectAmount, PerformTransactionDoesNotExist
from apps.billing.payme.models import MerchantTransactionsModel
from apps.billing.models import UserPayment, User, BankCard
from repository.auth_user import UserRepository
from apps.auth_user import constants as user_constants
from utils import choices, exceptions
from utils.payme import get_params


class SubscribeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    params = serializers.JSONField()

    def validate_id(self, value):
        try:
            UserRepository().get_user_by_uniq_id(value)
        except User.DoesNotExist:
            raise exceptions.NotFoundException(user_constants.USER_DOES_NOT_EXIST)
        return value


class VerifyCardSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    number = serializers.CharField(source='pan', required=True)
    code = serializers.CharField(max_length=6)

    class Meta:
        model = BankCard
        fields = (
            'id',
            'code',
            'number'
        )

    def validate_id(self, value):
        try:
            UserRepository().get_user_by_uniq_id(value)
        except User.DoesNotExist:
            raise exceptions.NotFoundException(user_constants.USER_DOES_NOT_EXIST)
        return value


class RemoveCardSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    number = serializers.CharField(source='pan', required=True)

    class Meta:
        model = BankCard
        fields = (
            'id',
            'number'
        )

    def validate_id(self, value):
        try:
            UserRepository().get_user_by_uniq_id(value)
        except User.DoesNotExist:
            raise exceptions.NotFoundException(user_constants.USER_DOES_NOT_EXIST)
        return value


class PaymeGeneratePayLinkSerializer(serializers.Serializer):
    order_id = serializers.CharField(max_length=255)
    amount = serializers.IntegerField(help_text="Сумма в тийинах")


class MerchantSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    method = serializers.CharField()
    params = serializers.JSONField()


class MerchantTransactionsModelSerializer(serializers.ModelSerializer):
    """
    MerchantTransactionsModelSerializer class \
        That's used to serialize merchant Transactions data.
    """
    start_date = serializers.IntegerField(allow_null=True)
    end_date = serializers.IntegerField(allow_null=True)
    order_id = serializers.CharField(source="order.id", allow_null=True, required=False)

    class Meta:
        # pylint: disable=missing-class-docstring
        model: MerchantTransactionsModel = MerchantTransactionsModel
        fields: str = "__all__"
        extra_fields = ['start_date', 'end_date']

    def validate(self, attrs) -> dict:
        """
        Validate the data given to the MerchantTransactionsModel.
        """
        if attrs.get("order", {}).get('id', None):
            try:
                order = UserPayment.objects.get(
                    id=attrs['order']['id']
                )
                if order.amount != int(attrs['amount']):
                    raise IncorrectAmount()

            except IncorrectAmount as error:
                raise IncorrectAmount() from error

        return attrs

    def validate_amount(self, amount) -> int:
        """
        Validator for Transactions Amount.
        """

        if amount:
            if int(amount) <= PAYME_MIN_AMOUNT:
                raise IncorrectAmount("Payment amount is less than allowed.")

        return amount

    def validate_order_id(self, order_id) -> UUID:
        """
        Use this method to check if a transaction is allowed to be executed.

        Parameters
        ----------
        order_id: str -> Order Indentation.
        """

        try:
            order_id = UUID(order_id)
            UserPayment.objects.filter(status__in=[
                choices.PaymentStatusChoices.PENDING,
                choices.PaymentStatusChoices.CREATE_TRANSACTION,
            ],
                is_active=True).get(id=order_id)
        except (UserPayment.DoesNotExist, ValueError) as error:
            raise PerformTransactionDoesNotExist() from error

        return order_id

    @classmethod
    def get_validated_data(cls, params: dict) -> dict:
        """
        This static method helps to get validated data.

        Parameters
        ----------
        params: dict — Includes request params.
        """
        serializer = cls(
            data=get_params(params)
        )
        serializer.is_valid(raise_exception=True)
        clean_data: dict = serializer.validated_data

        return clean_data
