from rest_framework import viewsets

from fix_the_news.api.pagination import CustomPageNumberPagination
from fix_the_news.api.topics import serializers
from fix_the_news.topics import models


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = CustomPageNumberPagination
    serializer_class = serializers.TopicReadOnlySerializer
    queryset = models.Topic.objects\
        .filter(active=True)\
        .order_by("-date_created")
