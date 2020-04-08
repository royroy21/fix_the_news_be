from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fix_the_news.api.topics.serializers import CategorySerializer
from fix_the_news.news_items import models


class NewsItemSerializer(serializers.ModelSerializer):

    serialized_category = serializers.SerializerMethodField()

    class Meta:
        model = models.NewsItem
        fields = (
            'category',
            'id',
            'title',
            'topic',
            'type',
            'serialized_category',
            'user',
            'url',
        )
        read_only_fields = (
            'id',
        )

    def get_serialized_category(self, obj):
        return CategorySerializer(obj.category).data

    def update(self, instance, validated_data):
        raise ValidationError("Cannot update")


class NewsTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NewsType
        fields = (
            'id',
            'title',
        )
        read_only_fields = fields
