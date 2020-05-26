from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class PageLimitOffset(PageNumberPagination):
    # # 默认每页显示的数据条数
    # default_limit = 5
    # # URL中传入的显示数据条数的参数
    # limit_query_param = 'limit'
    # # URL中传入的数据位置的参数
    # offset_query_param = 'offset'
    # # 最大每页显得条数
    # max_limit = None

    page_size = 10
    # 每页显示数据的数量
    max_page_size = 10
    # 每页最多可以显示的数据数量
    page_query_param = 'page'
    # 获取页码时用的参数
    page_size_query_param = 'size'
