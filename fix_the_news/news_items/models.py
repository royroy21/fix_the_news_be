from urllib.parse import urlparse

from django.db import models
from fix_the_news.core.models import DateCreatedUpdatedMixin
from fix_the_news.news_items.services.ranking_service import \
    NewsItemRankingService


class NewsItem(DateCreatedUpdatedMixin):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=254)
    topic = models.ForeignKey(
        "topics.Topic",
        on_delete=models.CASCADE,
        related_name="news_items",
    )
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    url = models.CharField(max_length=254)
    category = models.ForeignKey("topics.Category", on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    news_source = models.ForeignKey(
        "news_items.NewsSource",
        on_delete=models.CASCADE,
        related_name="news_items",
    )

    def __str__(self):
        return f"{self.title} ({self.topic})"

    class Meta:
        indexes = [
            models.Index(fields=['score']),
        ]

class NewsSourceManager(models.Manager):
    def get_or_create(self, *args, **kwargs):
        kwargs["hostname"] = urlparse(kwargs["hostname"]).hostname
        return super().get_or_create(*args, **kwargs)


class NewsSource(DateCreatedUpdatedMixin):
    objects = NewsSourceManager()
    hostname = models.CharField(max_length=254)
    formatted_name = models.CharField(max_length=254, blank=True, default="")

    def get_name(self):
        return self.formatted_name or self.hostname.lstrip("www.")

    def __str__(self):
        return f"{self.hostname} ({self.formatted_name or ' ?? '})"
