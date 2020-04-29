import logging

import requests
from requests import exceptions as requests_exceptions
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fix_the_news.api.topics.serializers import CategorySerializer
from fix_the_news.news_items import models

logger = logging.getLogger(__name__)


class NewsItemSerializer(serializers.ModelSerializer):
    news_source = serializers.SerializerMethodField()
    serialized_category = serializers.SerializerMethodField()

    class Meta:
        model = models.NewsItem
        fields = (
            'category',
            'id',
            'news_source',
            'title',
            'topic',
            'serialized_category',
            'user',
            'url',
        )
        read_only_fields = (
            'id',
        )

    def get_news_source(self, obj):
        return obj.news_source.get_name()

    def get_serialized_category(self, obj):
        return CategorySerializer(obj.category).data

    def create(self, validated_data):
        news_source, _ = models.NewsSource.objects\
            .get_or_create(hostname=validated_data["url"])
        validated_data["news_source"] = news_source
        return super().create(validated_data)

    def update(self, instance, validated_data):
        raise ValidationError("Cannot update")

    def validate_url(self, url):
        if url.startswith("http://"):
            url = url.replace("http://", "https://")
        elif not url.startswith("https://"):
            url = f"https://{url}"

        error_message = "Sorry URL provided was not valid"
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
