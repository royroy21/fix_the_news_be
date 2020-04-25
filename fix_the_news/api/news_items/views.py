from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from fix_the_news.api.news_items import serializers
from fix_the_news.api.views import CustomModelViewSet
from fix_the_news.news_items import models
from fix_the_news.topics import models as topics_models


class NewsItemViewSet(CustomModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = serializers.NewsItemSerializer
    queryset = models.NewsItem.objects\
        .filter(active=True)\
        .order_by("-date_created")

    ALL_PARAMS = [
        topics_models.Category.TYPE_FOR,
        topics_models.Category.TYPE_NEUTRAL,
        topics_models.Category.TYPE_AGAINST,
    ]

    def get_queryset(self):
        filters = {}
        category = self.request.query_params.get("category")
        if category:
            filters.update({"category__type": category})
        topic = self.request.query_params.get("topic")
        if topic:
            filters.update({"topic": topic})
        return super().get_queryset().filter(**filters)

    def create(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().create(*args, **kwargs)
