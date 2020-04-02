from django.db import models

from fix_the_news.core.models import DateCreatedUpdatedMixin


class NewsItem(DateCreatedUpdatedMixin):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=254)
    topic = models.ForeignKey(
        "topics.Topic",
        on_delete=models.CASCADE,
        related_name="news_items",
    )
    type = models.ForeignKey(
        "news_items.NewsType",
        on_delete=models.SET_DEFAULT,
        default=None,
    )
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    url = models.CharField(max_length=254)
    category = models.ForeignKey("topics.Category", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.topic})"


class NewsType(DateCreatedUpdatedMixin):
    title = models.CharField(max_length=254, unique=True)

    def __str__(self):
        return self.title
