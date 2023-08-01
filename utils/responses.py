from rest_framework.response import Response as BaseResponse

from utils.utils import get_json_data


class Response(BaseResponse):

    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None,
                 success: bool = True, error=None,
                 message: str = None):
        json_data = get_json_data(success, error, message, data)
        super().__init__(json_data, status, template_name, headers, exception, content_type)
