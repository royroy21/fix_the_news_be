from rest_framework import serializers

from fix_the_news.api.news_items.serializers import NewsItemSerializer
from fix_the_news.topics import models


class TopicSerializer(serializers.ModelSerializer):

    top_news_items = serializers.SerializerMethodField()

    class Meta:
        model = models.Topic
        fields = (
            "id",
            "title",
            "top_news_items",
            "user",
        )
        read_only_fields = fields

    def get_top_news_items(self, obj):
        return {
            key: NewsItemSerializer(
                    obj.get_top_news_items(key), many=True).data
            for key
            in models.Category.ALL_TYPE_CHOICES
        }
