from rest_framework.pagination import LimitOffsetPagination


class TitlePagination(LimitOffsetPagination):
    default_limit = 2
