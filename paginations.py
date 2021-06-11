from rest_framework.pagination import PageNumberPagination as DrfPageNumberPagination


class PageNumberPagination(DrfPageNumberPagination):
    # 默认一页显示的条数
    page_size = 11
    # url中携带页码的key
    page_query_param = 'p'
    # url中用户携带自定义一页条数的key
    page_size_query_param = 'ps'
    # 用户最大可自定义一页的条数
    max_page_size = 10
