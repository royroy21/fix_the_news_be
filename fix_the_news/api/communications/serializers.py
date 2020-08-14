from rest_framework import serializers

from fix_the_news.communications import models


class CommunicationReadOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Communication
        fields = (
            'text',
            'type',
        )
        read_only_fields = fields
