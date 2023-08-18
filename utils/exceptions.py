from rest_framework.exceptions import APIException


class CustomException(APIException):
    default_code = 'error'
    status_code = 400
    default_message = 'Something went wrong'
    detail = 'Something went wrong'

    def __init__(self, message=None, default_code=None, status_code=None):
        self.message = message if message else self.default_message
        self.default_code = default_code if default_code else self.default_code
        self.status_code = status_code if status_code else self.status_code
        self.detail = self.message


class NotAuthenticatedException(CustomException):
    default_code = 'not_authenticated'
    status_code = 401
    default_message = 'Not authenticated'


class BadRequestException(CustomException):
    default_code = 'bad_request'
    status_code = 400
    default_message = 'Bad request'


class NotFoundException(CustomException):
    default_code = 'not_found'
    status_code = 404
    default_message = 'Not found'
