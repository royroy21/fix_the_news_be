from django.db import models


class ActiveManager(models.Manager):

    def get_active(self):
        return self.model.objects.filter(active=True)
