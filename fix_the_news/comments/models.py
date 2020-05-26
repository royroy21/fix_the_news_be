from django.contrib.contenttypes.fields import \
    GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from fix_the_news.core.models import DateCreatedUpdatedMixin


class Comment(DateCreatedUpdatedMixin):
    active = models.BooleanField(default=True)
    comments = GenericRelation('comments.Comment')
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    text = models.TextField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return f'linked to {self.content_type.name}, {self.user.email}'
