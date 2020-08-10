from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from fix_the_news.api.news_items import serializers
from fix_the_news.api.pagination import CustomPageNumberPagination
from fix_the_news.api.views import CustomCreateRetrieveListViewSet
from fix_the_news.news_items import models


class NewsItemViewSet(CustomCreateRetrieveListViewSet):
    allowed_filters = [
        'category',
        'topic',
    ]
    pagination_class = CustomPageNumberPagination
    queryset = models.NewsItem.objects\
        .filter(active=True)\
        .order_by("-date_created")
    serializer_class = serializers.NewsItemSerializer

    def create(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().create(*args, **kwargs)

    @action(methods=['post'], detail=True, url_path='add-view')
    def add_view(self, request, *args, **kwargs):
        news_item = self.get_object()
        if not news_item:
            return Response(status=status.HTTP_404_NOT_FOUND)
        news_item.views += 1
        news_item.save()
        return Response(status=status.HTTP_200_OK)
