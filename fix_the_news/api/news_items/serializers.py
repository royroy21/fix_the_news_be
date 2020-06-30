from datetime import datetime, timedelta
import logging

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fix_the_news.api.topics.serializers import CategoryReadOnlySerializer
from fix_the_news.api.users.serializers import UserReadOnlySerializer
from fix_the_news.news_items import models
from fix_the_news.news_items.services import NewsItemURLService


logger = logging.getLogger(__name__)


class NewsItemSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    news_source = serializers.SerializerMethodField()
    serialized_category = serializers.SerializerMethodField()
    serialized_user = serializers.SerializerMethodField()
    topic_slug = serializers.SerializerMethodField()

    class Meta:
        model = models.NewsItem
        fields = (
            'category',
            'date_created',
            'id',
            'like',
            'likes_count',
            'news_source',
            'serialized_category',
            'serialized_user',
            'title',
            'topic',
            'topic_slug',
            'user',
            'url',
        )
        read_only_fields = (
            'id',
            'date_created',
            'like',
            'likes_count',
            'serialized_category',
            'serialized_user',
            'topic_slug',
        )

    def get_like(self, obj):
        """
        Returns like ID if user making the
        request liked this news item
        """
        user = self.context["request"].user
        if isinstance(user, AnonymousUser):
            return None
        query = obj.likes.filter(user=user)
        if query.exists():
            return query.first().id
        return None

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_news_source(self, obj):
        return obj.news_source.get_name()

    def get_serialized_category(self, obj):
        return CategoryReadOnlySerializer(obj.category).data

    def get_serialized_user(self, obj):
        return UserReadOnlySerializer(obj.user).data

    def get_topic_slug(self, obj):
        return obj.topic.slug

    def create(self, validated_data):
        news_source, _ = models.NewsSource.objects\
            .get_or_create(hostname=validated_data["url"])
        validated_data["news_source"] = news_source
        return super().create(validated_data)

    def validate(self, attrs):
        self.check_news_items_limit(attrs["user"])
        return super().validate(attrs)

    def check_news_items_limit(self, user):
        twenty_four_hours_ago = datetime.now() - timedelta(days=1)
        news_items_created = models.NewsItem.objects.filter(
            user=user,
            date_created__gte=twenty_four_hours_ago,
        )
        limit = settings.NEWS_ITEMS_LIMIT
        if news_items_created.count() >= limit:
            logger.error("NEWS_ITEMS_LIMIT reached")
            raise ValidationError({
                "non_field_errors": [f"You are limited to adding {limit} "
                                     f"news items within a 24 hour period"],
            })

    def validate_url(self, url):
        service = NewsItemURLService()
        parsed_url, error = service.parse_and_validate(url)
        if error:
            raise ValidationError(error)
        return parsed_url
