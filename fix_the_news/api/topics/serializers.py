from rest_framework import serializers

from fix_the_news.topics import models


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = (
            "id",
            "title",
            "type",
        )
        read_only_fields = fields


class TopicSerializer(serializers.ModelSerializer):

    categories = CategorySerializer(many=True)
    top_news_items = serializers.SerializerMethodField()

    class Meta:
        model = models.Topic
        fields = (
            "categories",
            "id",
            "title",
            "top_news_items",
            "user",
        )
        read_only_fields = fields

    def get_top_news_items(self, obj):
        from fix_the_news.api.news_items.serializers import NewsItemSerializer
        return {
            key: NewsItemSerializer(
                    obj.get_top_news_items(key), many=True).data
            for key
            in models.Category.ALL_TYPE_CHOICES
        }
