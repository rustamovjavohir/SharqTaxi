import uuid

from django.shortcuts import get_object_or_404

from apps.billing.models import BankCard, UserPayment
from apps.billing.payme.methods.cancel_transaction import CancelTransaction
from apps.billing.payme.methods.check_perform_transaction import CheckPerformTransaction
from apps.billing.payme.methods.check_transaction import CheckTransaction
from apps.billing.payme.methods.create_transaction import CreateTransaction
from apps.billing.payme.methods.get_statement import GetStatement
from apps.billing.payme.methods.perform_transaction import PerformTransaction
from apps.billing.payme.models import PaymeTransaction
from utils import choices
from utils.exceptions import NotFoundException
from apps.billing import constants


class PaymeRepository:
    def __init__(self):
        self.bank_card = BankCard
        self.user_payment = UserPayment

    def get_bank_card_by_number(self, number: str) -> BankCard:
        return get_object_or_404(self.bank_card, number=number)

    def create_bank_card(self, **kwargs) -> BankCard:
        return self.bank_card.objects.create(**kwargs)

    def id_2_uuid(self, order_id) -> uuid.UUID:
        try:
            return uuid.UUID(order_id)
        except ValueError:
            raise NotFoundException(constants.PAYMENT_NOT_FOUND)

    def get_active_payment_by_id(self, order_id) -> UserPayment:
        payment = self.user_payment.objects.filter(is_active=True, id=self.id_2_uuid(order_id),
                                                   status__in=(
                                                       choices.PaymentStatusChoices.PENDING,
                                                       choices.PaymentStatusChoices.CREATE_TRANSACTION)).first()
        if not payment:
            raise NotFoundException(constants.PAYMENT_NOT_FOUND)
        return payment


class PaymeMerchantRepository:
    available_methods: dict = {
        "CheckPerformTransaction": CheckPerformTransaction,
        "CreateTransaction": CreateTransaction,
        "PerformTransaction": PerformTransaction,
        "CancelTransaction": CancelTransaction,
        "CheckTransaction": CheckTransaction,
        "GetStatement": GetStatement
    }

    def __init__(self):
        self.model = PaymeTransaction
        self.user_payment = UserPayment

    def get_user_payment_by_id(self, order_id) -> UserPayment:
        return get_object_or_404(self.user_payment, id=order_id)

    def create_user_payment(self, **kwargs) -> UserPayment:
        return self.model.objects.create(**kwargs)

    def perform_transaction(self, order_id) -> None:
        self.user_payment.objects.filter(
            id=order_id, is_active=True
        ).update(
            status=choices.PaymentStatusChoices.PAID,
            payment_method=choices.PaymentTypeChoices.CARD
        )

    def create_transaction(self, order_id) -> None:
        self.user_payment.objects.filter(
            id=order_id, is_active=True
        ).update(
            status=choices.PaymentStatusChoices.CREATE_TRANSACTION
        )

    def cancel_user_payment(self, order_id) -> None:
        self.user_payment.objects.filter(
            id=order_id, is_active=True
        ).update(
            status=choices.PaymentStatusChoices.CANCELED
        )
