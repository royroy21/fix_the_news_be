from rest_framework import serializers
from fix_the_news.topics import models


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Topic
        fields = (
            'id',
            'title',
            'user',
        )
        read_only_fields = fields
