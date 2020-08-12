from django.db.models.signals import pre_save
from django.dispatch import receiver

from fix_the_news.communications import models


@receiver(pre_save, sender=models.Communication)
def inactivate_communications(sender, instance, **kwargs):
    sender.objects.filter(type=instance.type).update(active=False)
