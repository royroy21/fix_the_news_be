from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fix_the_news.api.users.serializers import UserReadOnlySerializer
from fix_the_news.comments import models


class BaseCommentSerializer(serializers.ModelSerializer):
    serialized_user = serializers.SerializerMethodField()

    def get_serialized_user(self, obj):
        return UserReadOnlySerializer(obj.user).data


class CommentSerializer(BaseCommentSerializer):
    content_type = None
    content_object = serializers.CharField(write_only=True)

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'content_object',
            'serialized_user',
            'text',
            'user',
        )
        read_only_fields = (
            'id',
        )

    def validate_content_object(self, content_object):
        query = self.content_type.objects.filter(id=content_object)
        if not query.exists():
            raise ValidationError(
                f'{self.content_type.__name__} '
                f'with id {content_object} does not exist',
            )
        return query.first()


class CommentReadOnlySerializer(BaseCommentSerializer):

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'serialized_user',
            'text',
            'user',
        )
        read_only_fields = fields
