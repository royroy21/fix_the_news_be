from django.db.models import Q
from rest_framework import authentication, permissions, viewsets, status
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

    PARAM_FOR = topics_models.Category.TYPE_FOR
    PARAM_NEUTRAL = topics_models.Category.TYPE_NEUTRAL
    PARAM_AGAINST = topics_models.Category.TYPE_AGAINST
    ALL_PARAMS = [
        PARAM_FOR,
        PARAM_NEUTRAL,
        PARAM_AGAINST,
    ]

    def get_queryset(self):
        categories_filters = Q()
        for param in self.ALL_PARAMS:
            query_param = self.request.query_params.get(param, None)
            if query_param:
                categories_filters = categories_filters \
                                     | Q(category__type=param)

        filters = {}
        topic = self.request.query_params.get("topic", None)
        if topic:
            filters.update({"topic": topic})

        return super().get_queryset().filter(categories_filters, **filters)

    def create(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().create(*args, **kwargs)


class NewsTypeViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.NewsTypeSerializer
    queryset = models.NewsType.objects.order_by("title")
