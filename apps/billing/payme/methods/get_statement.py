from django.db import DatabaseError

from apps.billing.payme.models import MerchantTransactionsModel
from api.billing.serializers.payme import MerchantTransactionsModelSerializer
from utils.logging import logger
from utils.payme import make_aware_datetime as mad


class GetStatement:
    model = MerchantTransactionsModel
    serializer = MerchantTransactionsModelSerializer
    """
    GetStatement class
    Transaction information is used for reconciliation
    of merchant and Payme Business transactions.

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-merchant-api/getstatement
    """

    def __call__(self, params: dict) -> tuple or dict:
        clean_data: dict = self.serializer.get_validated_data(
            params=params
        )

        start_date, end_date = mad(
            int(clean_data.get("start_date")),
            int(clean_data.get("end_date"))
        )

        try:
            transactions = \
                self.model.objects.filter(
                    created_at__gte=start_date,
                    created_at__lte=end_date
                )

            if not transactions:  # no transactions found for the period
                return {"result": {"transactions": []}}

            statements = [
                {
                    'id': t._id,
                    'time': int(t.created_at.timestamp()),
                    'amount': t.amount,
                    'account': {'order_id': t.order_id},
                    'create_time': t.state,
                    'perform_time': t.perform_time,
                    'cancel_time': t.cancel_time,
                    'transaction': t.order_id,
                    'state': t.state,
                    'reason': t.reason,
                    'receivers': []  # not implemented
                } for t in transactions
            ]

            response: dict = {
                "result": {
                    "transactions": statements
                }
            }
        except DatabaseError as error:
            logger.error("Error getting transaction in database: %s", error)
            response = {"result": {"transactions": []}}

        return None, response
