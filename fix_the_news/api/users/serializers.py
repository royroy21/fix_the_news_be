import logging

from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.transaction import on_commit
from django.utils.translation import ugettext_lazy as _
from djoser.serializers import UserSerializer as DjoserUserSerializer
from djoser.serializers import UserCreateSerializer as \
    DjoserUserCreateSerializer
from rest_framework import serializers
from rest_framework.serializers import CharField

from fix_the_news.users.tasks import create_avatar_thumbnail

logger = logging.getLogger(__name__)
User = get_user_model()


class CurrentUserSerializer(DjoserUserSerializer):
    avatar = serializers.ImageField(
        allow_empty_file=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            "avatar",
            "avatar_thumbnail_small",
            "id",
            "first_name",
            "last_name",
        )
        read_only_fields = (
            "avatar_thumbnail_small",
            "id",
        )

    def save(self, **kwargs):
        user = super().save(**kwargs)
        try:
            if "avatar" in self.validated_data:
                on_commit(lambda: create_avatar_thumbnail.delay(user.id))
        except Exception as error:
            logger.error('RABBIT IMAGE UPLOAD ERROR %s', error)

        return user


class CreatePasswordRetypeSerializer(DjoserUserCreateSerializer):

    re_password = CharField(
        style={'input_type': 'password'},
        write_only=True,
    )

    default_error_messages = {
        'password_mismatch': _('Password fields do not match.'),
    }

    class Meta:
        model = User
        fields = (
            settings.LOGIN_FIELD,
            "avatar",
            "password",
            "re_password",
            "first_name",
            "last_name",
        )

    def validate(self, attrs):
        re_password = attrs.pop('re_password')
        attrs = super().validate(attrs)
        if attrs['password'] != re_password:
            self.fail('password_mismatch')
        return attrs

    def save(self, **kwargs):
        user = super().save(**kwargs)
        if "avatar" in self.validated_data:
            on_commit(lambda: create_avatar_thumbnail.delay(user.id))
        return user


class UserReadOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            "avatar",
            "avatar_thumbnail_small",
            "id",
            "first_name",
            "last_name",
        )
        read_only_fields = fields
