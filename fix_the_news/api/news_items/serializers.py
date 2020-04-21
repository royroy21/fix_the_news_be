from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fix_the_news.api.topics.serializers import CategorySerializer
from fix_the_news.news_items import models


class NewsItemSerializer(serializers.ModelSerializer):
    news_source = serializers.SerializerMethodField()
    serialized_category = serializers.SerializerMethodField()
    serialized_type = serializers.SerializerMethodField()

    class Meta:
        model = models.NewsItem
        fields = (
            'category',
            'id',
            'news_source',
            'title',
            'topic',
            'type',
            'serialized_category',
            'serialized_type',
            'user',
            'url',
        )
        read_only_fields = (
            'id',
        )

    def get_serialized_category(self, obj):
        return CategorySerializer(obj.category).data

    def get_serialized_type(self, obj):
        return NewsTypeSerializer(obj.type).data

    def get_news_source(self, obj):
        return obj.news_source.get_name()

    def create(self, validated_data):
        news_source, _ = models.NewsSource.objects\
            .get_or_create(hostname=validated_data["url"])
        validated_data["news_source"] = news_source
        return super().create(validated_data)

    def update(self, instance, validated_data):
        raise ValidationError("Cannot update")

    def validate_url(self, url):
        # TODO - check if url is valid here?
        if url.startswith("http://"):
            return url.replace("http://", "https://")
        elif not url.startswith("https://"):
            return f"https://{url}"
        else:
            return url


class NewsTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NewsType
        fields = (
            'id',
            'title',
        )
        read_only_fields = fields
