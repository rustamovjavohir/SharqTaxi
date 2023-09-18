from rest_framework.exceptions import APIException
from utils.exceptions import CustomException


class CustomValidationError(CustomException):
    default_code = 'invalid'
    status_code = 400
    message = 'Invalid input.'
    detail = "Invalid input2."
