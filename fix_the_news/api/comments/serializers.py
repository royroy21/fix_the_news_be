from rest_framework import serializers

from fix_the_news.api.users.serializers import UserReadOnlySerializer
from fix_the_news.comments import models


class CommentSerializer(serializers.ModelSerializer):
    serialized_user = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'comment',
            'news_item',
            'serialized_user',
            'text',
            'user',
        )
        read_only_fields = (
            'id',
        )

    def get_serialized_user(self, obj):
        return UserReadOnlySerializer(obj.user).data
