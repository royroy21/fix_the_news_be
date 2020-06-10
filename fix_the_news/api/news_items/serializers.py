import logging

import requests
from requests import exceptions as requests_exceptions
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fix_the_news.api.topics.serializers import CategoryReadOnlySerializer
from fix_the_news.api.users.serializers import UserReadOnlySerializer
from fix_the_news.news_items import models

logger = logging.getLogger(__name__)


class NewsItemSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    news_source = serializers.SerializerMethodField()
    serialized_category = serializers.SerializerMethodField()
    serialized_user = serializers.SerializerMethodField()

    class Meta:
        model = models.NewsItem
        fields = (
            'category',
            'date_created',
            'id',
            'likes_count',
            'news_source',
            'serialized_category',
            'serialized_user',
            'title',
            'topic',
            'user',
            'url',
        )
        read_only_fields = (
            'id',
            'date_created',
            'likes_count',
            'serialized_category',
            'serialized_user',
        )

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_news_source(self, obj):
        return obj.news_source.get_name()

    def get_serialized_category(self, obj):
        return CategoryReadOnlySerializer(obj.category).data

    def get_serialized_user(self, obj):
        return UserReadOnlySerializer(obj.user).data

    def create(self, validated_data):
        news_source, _ = models.NewsSource.objects\
            .get_or_create(hostname=validated_data["url"])
        validated_data["news_source"] = news_source
        return super().create(validated_data)

    def validate_url(self, url):
        if url.startswith("http://"):
            url = url.replace("http://", "https://")
        elif not url.startswith("https://"):
            url = f"https://{url}"

        error_message = "URL provided was not valid"
        try:
            response = requests.get(url)
        except (
            requests_exceptions.ConnectionError,
            requests_exceptions.ConnectTimeout,
            requests_exceptions.SSLError,
        ) as error:
            logger.error(f"Problem validating URL:{url} {error}")
            raise ValidationError(error_message)
        if not response.ok:
            raise ValidationError(error_message)

        return url
