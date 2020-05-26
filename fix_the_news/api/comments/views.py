from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from fix_the_news.api.comments import serializers
from fix_the_news.api.pagination import CustomPageNumberPagination
from fix_the_news.api.views import CustomModelViewSet
from fix_the_news.comments import models
from fix_the_news.news_items import models as news_items_models


class CommentViewSet(CustomModelViewSet):
    pagination_class = CustomPageNumberPagination
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects\
        .filter(active=True)\
        .order_by("-date_created")

    def create(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().create(request, *args, **kwargs)

    @action(methods=['post'], detail=False, url_path='comment')
    def link_to_comment(self, request):
        self.serializer_class.content_type = models.Comment
        return self.create(request)

    @action(methods=['post'], detail=False, url_path='news-item')
    def link_to_news_item(self, request):
        self.serializer_class.content_type = news_items_models.NewsItem
        return self.create(request)
