import uuid
import time
import datetime

from apps.billing.models import UserPayment
from apps.billing.payme.exceptions import TooManyRequests
from api.billing.serializers.payme import MerchantTransactionsModelSerializer
from apps.billing.payme.models import MerchantTransactionsModel

from utils.logging import logger
from utils.payme import get_params


class CreateTransaction:
    model = MerchantTransactionsModel
    serializer = MerchantTransactionsModelSerializer
    order_model = UserPayment
    """
    CreateTransaction class
    That's used to create transaction

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-merchant-api/createtransaction
    """

    def __call__(self, params: dict) -> tuple:
        response: dict = {}
        serializer = self.serializer(
            data=get_params(params)
        )
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data.get("order").get('id')
        order = self.order_model.objects.filter(
            id=order_id
        ).first()

        try:
            transaction = self.model.objects.filter(
                order=order
            ).last()

            if transaction:
                if transaction._id != serializer.validated_data.get("_id"):
                    raise TooManyRequests()

        except TooManyRequests as error:
            logger.error("Too many requests for transaction %s", error)
            raise TooManyRequests() from error

        if transaction is None:
            transaction, _ = \
                self.model.objects.get_or_create(
                    _id=serializer.validated_data.get('_id'),
                    order=order,
                    transaction_id=uuid.uuid4(),
                    amount=serializer.validated_data.get('amount'),
                    created_at_ms=int(time.time() * 1000),
                )

        if transaction:
            response: dict = {
                "result": {
                    "create_time": int(transaction.created_at_ms),
                    "transaction": transaction.transaction_id,
                    "state": int(transaction.state),
                }
            }

        return order_id, response

    @staticmethod
    def _convert_ms_to_datetime(time_ms: int) -> datetime:
        """Use this format to convert from time ms to datetime format.
        """
        readable_datetime = datetime.datetime.fromtimestamp(time_ms / 1000)

        return readable_datetime
