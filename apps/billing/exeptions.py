from utils.exceptions import CustomException


class IncorrectAmount(CustomException):
    """
    IncorrectAmount class \
        That's used to raise exception when amount is incorrect.
    """
    default_detail = "Incorrect amount"
    default_code = "incorrect_amount"
    default_message = "Incorrect amount"

