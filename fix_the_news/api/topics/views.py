from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from fix_the_news.api.topics import serializers
from fix_the_news.topics import models


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = serializers.TopicSerializer
    queryset = models.Topic.objects\
        .get_active()\
        .order_by("-date_created")
