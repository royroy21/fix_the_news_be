from rest_framework import serializers
from fix_the_news.likes import models


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Like
        fields = (
            'id',
            'comment',
            'date_created',
            'news_item',
            'topic',
            'user',
        )
        read_only_fields = (
            'id',
            'date_created',
        )
