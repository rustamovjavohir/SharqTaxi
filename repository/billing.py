import uuid

from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.billing.models import BankCard, UserPayment
from apps.billing.payme.methods.cancel_transaction import CancelTransaction
from apps.billing.payme.methods.check_perform_transaction import CheckPerformTransaction
from apps.billing.payme.methods.check_transaction import CheckTransaction
from apps.billing.payme.methods.create_transaction import CreateTransaction
from apps.billing.payme.methods.get_statement import GetStatement
from apps.billing.payme.methods.perform_transaction import PerformTransaction
from apps.billing.payme.models import PaymeTransaction
from utils import choices
from utils.exceptions import NotFoundException, BadRequestException
from apps.billing import constants


class PaymeRepository:
    def __init__(self):
        self.bank_card = BankCard
        self.user_payment = UserPayment

    def get_bank_card_by_number(self, pan: str) -> BankCard:
        return get_object_or_404(self.bank_card, pan=pan)

    def get_bank_card_by_token(self, token: str) -> BankCard:
        return get_object_or_404(self.bank_card, token=token)

    def create_bank_card(self, **kwargs) -> BankCard:
        if self.bank_card.objects.filter(pan=kwargs.get('pan')).exists():
            raise BadRequestException(constants.BANK_CARD_ALREADY_EXISTS)
        return self.bank_card.objects.update_or_create(**kwargs)

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

    def change_card_status(self, pan: str, status: choices.BankCardStatusChoices) -> None:
        self.bank_card.objects.filter(pan=pan).update(status=status, updated_at=timezone.now())

    def in_or_active_card(self, pan: str, active: bool) -> None:
        self.bank_card.objects.filter(pan=pan).update(is_active=active, updated_at=timezone.now())


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
