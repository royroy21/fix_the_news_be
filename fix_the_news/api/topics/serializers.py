from rest_framework import serializers
from fix_the_news.topics import models


class CategoryReadOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = (
            'id',
            'title',
            'type',
        )
        read_only_fields = fields


class TopicReadOnlySerializer(serializers.ModelSerializer):

    comments_count = serializers.SerializerMethodField()
    serialized_categories = serializers.SerializerMethodField()
    news_items_count = serializers.SerializerMethodField()
    top_news_items = serializers.SerializerMethodField()

    class Meta:
        model = models.Topic
        fields = (
            'id',
            'comments_count',
            'date_created',
            'news_items_count',
            'serialized_categories',
            'slug',
            'title',
            'top_news_items',
            'user',
        )
        read_only_fields = fields

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_news_items_count(self, obj):
        return {
            key: obj.news_items.filter(active=True, category__type=key).count()
            for key
            in models.Category.ALL_TYPE_CHOICES
        }

    def get_serialized_categories(self, obj):
        """ Returns serialized categories sorted by category type choices """
        data_with_key = {
            category["type"]: category
            for category
            in CategoryReadOnlySerializer(obj.categories.all(), many=True).data
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
                obj.get_top_news_items(key),
                many=True,
                context=self.context).data
            for key
            in models.Category.ALL_TYPE_CHOICES
        }
