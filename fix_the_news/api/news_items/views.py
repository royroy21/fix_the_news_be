from rest_framework import authentication, permissions, viewsets

from fix_the_news.api.news_items import serializers
from fix_the_news.news_items import models


class NewsTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.NewsTypeSerializer
    queryset = models.NewsType.objects.order_by("title")
