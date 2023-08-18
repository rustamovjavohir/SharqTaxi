from api.billing.serializers.payme import MerchantTransactionsModelSerializer
from utils.payme import get_params

class CheckPerformTransaction:
    serializer = MerchantTransactionsModelSerializer
    """
    CheckPerformTransaction class
    That's used to check perform transaction.

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-merchant-api/checktransaction
    """

    def __call__(self, params: dict) -> tuple:
        serializer = self.serializer(
            data=get_params(params)
        )
        serializer.is_valid(raise_exception=True)

        response = {
            "result": {
                "allow": True,
                "additional": {
                    "order_name": "Order 33"
                },
                "detail": {
                    "amount": 1000,
                    "account": "12345678901234567890",
                    "code": "1234"
                }
            }
        }

        return None, response
