import csv
from django.core.management.base import BaseCommand

from fix_the_news.news_items.models import NewsType


class Command(BaseCommand):
    NEWS_TYPE_FILE = "/code/fix_the_news/news_items/data/news_types.csv"
    help = 'Creates news types from {}'.format(NEWS_TYPE_FILE)

    def handle(self, *args, **options):
        with open(self.NEWS_TYPE_FILE) as f:
            news_types = [
                NewsType(title=title.capitalize())
                for title, _ in csv.reader(f)
            ]
            self.stdout.write(self.style.SUCCESS(
                f"creating {len(news_types)} new news types"
            ))
            NewsType.objects.bulk_create(news_types)
            self.stdout.write(self.style.SUCCESS("finished"))
