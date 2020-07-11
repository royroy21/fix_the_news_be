from celery import shared_task

from fix_the_news.core.services import image_thumbnail_service
from fix_the_news.users import models


@shared_task
def create_avatar_thumbnail(user_id):
    user = models.User.objects.get(id=user_id)
    image_thumbnail_service.ImageThumbnailService()\
        .create_thumbnail(user, "avatar", "avatar_thumbnail_small")
