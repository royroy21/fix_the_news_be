from django.db import models
from django.utils.text import slugify

from fix_the_news.core.models import DateCreatedUpdatedMixin
from fix_the_news.topics.services import scoring_service


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
    ALL_TYPE_CHOICES = [
        type_choice
        for type_choice, _
        in TYPE_CHOICES
    ]
    type = models.CharField(
        choices=TYPE_CHOICES,
        default=TYPE_NEUTRAL,
        max_length=7,
    )
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.title} ({self.type}) ({self.topic})"


class Topic(DateCreatedUpdatedMixin):
    active = models.BooleanField(default=True)
    # If True this moves topic above all
    # other topics regardless of score
    priority = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)
    slug = models.CharField(max_length=254, unique=True)
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

    def create_missing_categories(self):
        topic_categories = self.categories.values_list("type", flat=True)
        missing_categories = [
            Category(topic=self, type=category_type, user=self.user)
            for category_type, _
            in Category.TYPE_CHOICES
            if category_type not in topic_categories
        ]
        return Category.objects.bulk_create(missing_categories)

    def get_top_news_items(self, category, amount=3):
        return self.news_items\
            .filter(active=True, category__type=category)\
            .order_by("-score", "-date_created")[:amount]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_score(self):
        return scoring_service.TopicScoringService().get_score(self)

    def save_score(self):
        self.score = self.get_score()
        self.save()
