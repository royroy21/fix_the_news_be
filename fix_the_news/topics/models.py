from django.db import models

from fix_the_news.core.models import DateCreatedUpdatedMixin


class Category(DateCreatedUpdatedMixin):
    title = models.CharField(max_length=254)
    topic = models.ForeignKey(
        "topics.Topic",
        on_delete=models.CASCADE,
        related_name="categories",
    )
    TYPE_FOR = "for"
    TYPE_NEUTRAL = "neutral"
    TYPE_AGAINST = "against"
    TYPE_CHOICES = [
        (TYPE_FOR, "For"),
        (TYPE_NEUTRAL, "Neutral"),
        (TYPE_AGAINST, "Against"),
    ]
    type = models.CharField(
        choices=TYPE_CHOICES,
        default=TYPE_NEUTRAL,
        max_length=7,
    )
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.type}) ({self.topic})"


class Topic(DateCreatedUpdatedMixin):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=254, unique=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.user})"

    def check_all_categories_exist(self):
        topic_categories = self.categories.values_list("type", flat=True)
        all_categories = [
            category_type
            for category_type, _
            in Category.TYPE_CHOICES
        ]
        return sorted(topic_categories) == sorted(all_categories)
