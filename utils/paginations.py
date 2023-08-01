from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BasePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data, success=True, error=None, message=None):
        return Response(OrderedDict([
            ('success', success),
            ('error', error),
            ('message', message),
            ('count', self.page.paginator.count),
            ('current', self.page.number),
            ('per_page', self.page_size),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
