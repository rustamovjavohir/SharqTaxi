from utils.paginations import BasePagination


class BillingPagination(BasePagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
