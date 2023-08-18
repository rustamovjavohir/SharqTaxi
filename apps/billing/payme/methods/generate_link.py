import base64
from decimal import Decimal
from dataclasses import dataclass

from apps.billing.payme.config import MERCHANT_ID, PAYME_CALLBACK_URL, PAYME_URL, KEY_1


@dataclass
class GeneratePayLink:
    """
    GeneratePayLink dataclass
    That's used to generate pay lint for each order.

    Parameters
    ----------
    order_id: int — The order_id for paying
    amount: int — The amount belong to the order

    Returns str — pay link
    ----------------------

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/initsializatsiya-platezhey/
    """
    order_id: str
    amount: Decimal

    def generate_link(self) -> str:
        """
        GeneratePayLink for each order.
        """
        generated_pay_link: str = "{payme_url}/{encode_params}"
        params: str = 'm={payme_id};ac.{payme_account}={order_id};a={amount};c={call_back_url}'

        params = params.format(
            payme_id=MERCHANT_ID,
            payme_account=KEY_1,
            order_id=self.order_id,
            amount=self.amount,
            call_back_url=PAYME_CALLBACK_URL
        )
        encode_params = base64.b64encode(params.encode("utf-8"))
        return generated_pay_link.format(
            payme_url=PAYME_URL,
            encode_params=str(encode_params, 'utf-8')
        )

    @staticmethod
    def to_soum(amount: Decimal) -> Decimal:
        """
        Convert from tiyin to soum.

        Parameters
        ----------
        amount: Decimal -> order amount
        """
        return amount * 100

    @staticmethod
    def to_tiyin(amount: Decimal) -> Decimal:
        """
        Convert from tiyin to soum.

        Parameters
        ----------
        amount: Decimal -> order amount
        """
        return amount / 100
