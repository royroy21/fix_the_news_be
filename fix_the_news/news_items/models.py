from urllib.parse import urlparse

from django.db import models
from django.contrib.postgres import fields as postgres_fields
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
    score_data = postgres_fields.JSONField(default=dict)
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

    def get_score(self):
        return NewsItemRankingService().get_total_score(self)

    def save_score(self):
        self.score_data = self.get_score()
        self.score = self.score_data['total_score']
        self.save()

    def get_highest_competing_score(self):
        """
        Gets highest competing score for news items
        for the same topic in the same category
        """
        return self.topic\
            .news_items.filter(category=self.category)\
            .order_by('-score')\
            .first()\
            .score


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
