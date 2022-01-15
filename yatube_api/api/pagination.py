from rest_framework.pagination import PageNumberPagination

class YatubePagination(PageNumberPagination):
    page_size = 20
