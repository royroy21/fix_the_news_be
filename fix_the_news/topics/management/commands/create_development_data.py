import csv

from django.core.management.base import BaseCommand

from fix_the_news.news_items import models as news_items_models
from fix_the_news.topics import models as topics_models
from fix_the_news.users import models as users_models


class Command(BaseCommand):
    DATA_FILE = "/code/fix_the_news/topics/data/development_test_data.csv"
    help = f"Creates test data for development environment from {DATA_FILE}"

    def handle(self, *args, **options):
        news_item_type, _ = \
            news_items_models.NewsType.objects.get_or_create(title="Article")

        with open(self.DATA_FILE) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                user, _ = users_models.User.objects.get_or_create(**{
                    "email": row["email"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                })
                topic, _ = topics_models.Topic.objects.get_or_create(**{
                    "user": user,
                    "title": row["topic_title"],
                })
                category, _ = topics_models.Category.objects.get_or_create(**{
                    "user": user,
                    "topic": topic,
                    "type": row["topic_category"],
                })
                news_item_title = row["news_item_title"]
                news_items_models.NewsItem.objects.get_or_create(**{
                    "title": news_item_title,
                    "topic": topic,
                    "type": news_item_type,
                    "user": user,
                    "url": row["news_item_url"],
                    "category": category,
                })
                self.stdout.write(self.style.SUCCESS(
                    f"Created news item: {news_item_title}"
                ))
