from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fix_the_news.news_items import models


class NewsTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NewsType
        fields = (
            'id',
            'title',
        )
        read_only_fields = fields

    def create(self, validated_data):
        raise ValidationError("Cannot create")

    def update(self, instance, validated_data):
        raise ValidationError("Cannot update")
