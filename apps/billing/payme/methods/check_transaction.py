from django.db import DatabaseError

from apps.billing.payme.exceptions import PerformTransactionDoesNotExist
from apps.billing.payme.models import MerchantTransactionsModel
from api.billing.serializers.payme import MerchantTransactionsModelSerializer
from utils.logging import logger


class CheckTransaction:
    model = MerchantTransactionsModel
    serializer = MerchantTransactionsModelSerializer
    """
    CheckTransaction class
    That's used to check transaction

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-merchant-api/checkperformtransaction
    """

    def __call__(self, params: dict) -> tuple or dict:
        response: dict = {}
        clean_data: dict = self.serializer.get_validated_data(
            params=params
        )

        try:
            transaction = \
                self.model.objects.get(
                    _id=clean_data.get("_id"),
                )
            response = {
                "result": {
                    "create_time": int(transaction.created_at_ms),
                    "perform_time": transaction.perform_time,
                    "cancel_time": transaction.cancel_time,
                    "transaction": transaction.transaction_id,
                    "state": transaction.state,
                    "reason": None,
                }
            }
            if transaction.reason:
                response["result"]["reason"] = int(transaction.reason)

        except DatabaseError as error:
            logger.error("Error getting transaction in database: %s", error)
        except self.model.DoesNotExist as error:
            raise PerformTransactionDoesNotExist from error
        return None, response
