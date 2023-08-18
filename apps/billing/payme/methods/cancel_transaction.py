import time

from django.db import transaction

from apps.billing import constants
from apps.billing.payme.models import MerchantTransactionsModel
from apps.billing.payme.exceptions import PerformTransactionDoesNotExist
from api.billing.serializers.payme import MerchantTransactionsModelSerializer


class CancelTransaction:
    model = MerchantTransactionsModel
    serializer = MerchantTransactionsModelSerializer
    """
    CancelTransaction class
    That is used to cancel a transaction.

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-merchant-api/canceltransaction
    """

    @transaction.atomic
    def __call__(self, params: dict) -> tuple:
        clean_data: dict = self.serializer.get_validated_data(
            params=params
        )
        try:
            with transaction.atomic():
                transactions = \
                    self.model.objects.filter(
                        _id=clean_data.get('_id'),
                    ).first()
                if transactions.cancel_time == 0:
                    transactions.cancel_time = int(time.time() * 1000)
                if transactions.perform_time == 0:
                    transactions.state = constants.PAYME_TRANSACTION_CANCELLED
                if transactions.perform_time != 0:
                    transactions.state = constants.PAYME_TRANSACTION_CANCELLED_AFTER_COMPLETE
                transactions.reason = clean_data.get("reason")
                transactions.save()

        except PerformTransactionDoesNotExist as error:
            raise PerformTransactionDoesNotExist() from error

        response: dict = {
            "result": {
                "state": transactions.state,
                "cancel_time": transactions.cancel_time,
                "transaction": transactions.transaction_id,
                "reason": int(transactions.reason),
            }
        }

        return transactions.order_id, response
