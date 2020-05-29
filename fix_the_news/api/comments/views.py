from rest_framework import status
from rest_framework.response import Response

from fix_the_news.api.comments import serializers
from fix_the_news.api.pagination import CustomPageNumberPagination
from fix_the_news.api.views import CustomCreateRetrieveListViewSet
from fix_the_news.comments import models


class CommentViewSet(CustomCreateRetrieveListViewSet):
    pagination_class = CustomPageNumberPagination
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects\
        .filter(active=True)\
        .order_by("-date_created")

    def get_queryset(self):
        filters = {}
        category = self.request.query_params.get("category")
        if category:
            filters.update({"category": category})
        topic = self.request.query_params.get("news_item")
        if topic:
            filters.update({"news_item": topic})
        return super().get_queryset().filter(**filters)

    def create(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().create(request, *args, **kwargs)
