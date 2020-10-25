from fix_the_news.api.pagination import CustomPageNumberPagination
from fix_the_news.api.topics import serializers
from fix_the_news.api.views import CustomCreateRetrieveListViewSet
from fix_the_news.topics import models


class TopicViewSet(CustomCreateRetrieveListViewSet):
    lookup_field = "slug"
    pagination_class = CustomPageNumberPagination
    serializer_class = serializers.TopicSerializer
    queryset = models.Topic.objects\
        .filter(active=True)\
        .order_by("-priority", "-score", "-date_created")
