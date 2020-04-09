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

    serialized_categories = serializers.SerializerMethodField()
    news_items_count = serializers.SerializerMethodField()
    top_news_items = serializers.SerializerMethodField()

    class Meta:
        model = models.Topic
        fields = (
            "id",
            "news_items_count",
            "serialized_categories",
            "title",
            "top_news_items",
            "user",
        )
        read_only_fields = fields

    def get_news_items_count(self, obj):
        return {
            key: obj.news_items.get_active().filter(
                category__type=key).count()
            for key
            in models.Category.ALL_TYPE_CHOICES
        }

    def get_serialized_categories(self, obj):
        """ Returns serialized categories sorted by category type choices """
        data_with_key = {
            category["type"]: category
            for category
            in CategorySerializer(obj.categories.all(), many=True).data
        }
        return [
            data_with_key[category_type]
            for category_type, _
            in models.Category.TYPE_CHOICES
        ]

    def get_top_news_items(self, obj):
        from fix_the_news.api.news_items.serializers import NewsItemSerializer
        return {
            key: NewsItemSerializer(
                    obj.get_top_news_items(key), many=True).data
            for key
            in models.Category.ALL_TYPE_CHOICES
        }
