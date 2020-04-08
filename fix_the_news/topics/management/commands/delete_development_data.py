import csv
from django.core.management.base import BaseCommand
from fix_the_news.users import models as users_models


class Command(BaseCommand):
    DATA_FILE = "/code/fix_the_news/core/data/development_test_data.csv"
    help = f"Deletes test data created by create_development_data"

    def handle(self, *args, **options):
        with open(self.DATA_FILE) as csv_file:
            user_emails = set([
                row["email"]
                for row
                in csv.DictReader(csv_file)
            ])
            users_models.User.objects\
                .filter(email__in=user_emails)\
                .delete()

        formatted_emails = ", ".join(user_emails)
        self.stdout.write(self.style.SUCCESS(
            f"Deleted data for users: {formatted_emails}"
        ))