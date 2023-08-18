import base64
import binascii
from decimal import Decimal

import requests
from django.core.exceptions import ValidationError

from apps.billing import constants
from apps.billing.exeptions import IncorrectAmount
from apps.billing.payme.config import (AUTHORIZATION, PAYME_URL, MERCHANT_KEY)
from apps.billing.payme.exceptions import (PermissionDenied, MethodNotFound, PerformTransactionDoesNotExist)
from apps.billing.payme.methods.cancel_transaction import CancelTransaction
from apps.billing.payme.methods.create_transaction import CreateTransaction
from apps.billing.payme.methods.generate_link import GeneratePayLink
from apps.billing.payme.methods.perform_transaction import PerformTransaction
from repository.billing import PaymeRepository, PaymeMerchantRepository
from apps.billing.payme import methods


class PaymeService:
    merchant_key = MERCHANT_KEY
    gen_link_class = GeneratePayLink

    def __init__(self):
        self.payme_repository = PaymeRepository()

    def create_card(self, **kwargs):
        data = dict(
            id=kwargs['id'],
            method=methods.CARD_CREATE,
            params=dict(
                card=dict(
                    number=kwargs['params']['card']['number'],
                    expire=kwargs['params']['card']['expire'],
                ),
                amount=kwargs['params']['amount'],
                save=kwargs['params']['save']
            )
        )
        response = requests.post(PAYME_URL, json=data, headers=AUTHORIZATION)
        result = response.json()
        if 'error' in result:
            return result

        token = result['result']['card']['token']
        return self.get_card_verify_code(token)

    def get_card_verify_code(self, token):
        self.payme_repository.get_bank_card_by_number(token)  # TODO: remove this line
        data = dict(
            method=methods.CARD_GET_VERIFY_CODE,
            params=dict(
                token=token
            )
        )
        response = requests.post(PAYME_URL, json=data, headers=AUTHORIZATION)
        result = response.json()
        if 'error' in result:
            return result

        result.update(token=token)
        return result

    def generate_pay_link(self, order_id: str, amount: Decimal):
        """Generate pay link for each order for payme."""
        payment = self.payme_repository.get_active_payment_by_id(order_id)
        if payment.amount != amount:
            raise IncorrectAmount(constants.INCORRECT_AMOUNT)
        return self.gen_link_class(order_id, amount).generate_link()


class PaymeMerchantService:
    merchant_key = MERCHANT_KEY

    def __init__(self):
        self.payme_repository = PaymeMerchantRepository()

    def call_back(self, request):
        password = request.META.get('HTTP_AUTHORIZATION')
        action = {}
        if self.authorize(password):
            incoming_data: dict = request.data
            incoming_method: str = incoming_data.get("method")

            try:
                payme_method = self.get_payme_method_by_name(incoming_method)
            except ValidationError as exc:
                raise MethodNotFound() from exc
            except PerformTransactionDoesNotExist as exc:
                raise PerformTransactionDoesNotExist() from exc

            order_id, action = payme_method(incoming_data.get("params"))

            if isinstance(payme_method, CreateTransaction):
                self.create_transaction(order_id, action)

            elif isinstance(payme_method, PerformTransaction):
                self.perform_transaction(order_id, action)

            elif isinstance(payme_method, CancelTransaction):
                self.cancel_transaction(order_id, action)

        return action

    def authorize(self, password) -> bool:
        """
        Authorize merchant by password.
        :param password: str
        """
        is_payme: bool = False

        if not isinstance(password, str):
            error = "Request from an unauthorized source!"
            raise PermissionDenied(error_message=error)

        password = password.split()[-1]

        try:
            password = base64.b64decode(password).decode('utf-8')
        except (binascii.Error, UnicodeDecodeError) as exc:
            error = "Error when authorize request to merchant!"
            raise PermissionDenied(error_message=error) from exc

        merchant_key = password.split(':')[-1]
        if merchant_key == self.merchant_key:
            is_payme = True

        if is_payme is False:
            raise PermissionDenied(
                error_message="Unavailable data for unauthorized users!"
            )
        return is_payme

    def get_payme_method_by_name(self, incoming_method):
        try:
            merchant_method = self.payme_repository.available_methods[incoming_method]
        except Exception as exc:
            error = f"Unavailable method: {incoming_method}"
            raise MethodNotFound(error_message=error) from exc

        return merchant_method()

    def create_transaction(self, order_id, action):
        self.payme_repository.create_transaction(order_id)
        print(f"create_transaction for order_id: {order_id}, response: {action}")

    def perform_transaction(self, order_id, action):
        self.payme_repository.perform_transaction(order_id)
        print(f"perform_transaction for order_id: {order_id}, response: {action}")

    def cancel_transaction(self, order_id, action):
        self.payme_repository.cancel_user_payment(order_id)
        print(f"cancel_transaction for order_id: {order_id}, response: {action}")
