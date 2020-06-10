from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fix_the_news.api.topics.serializers import CategoryReadOnlySerializer
from fix_the_news.api.users.serializers import UserReadOnlySerializer
from fix_the_news.news_items import models
from fix_the_news.news_items.services import NewsItemURLService


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
        service = NewsItemURLService()
        parsed_url = service.parse(url)
        error = service.validate(parsed_url)
        if error:
            raise ValidationError(error)
        return parsed_url
