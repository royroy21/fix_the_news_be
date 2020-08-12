from datetime import timedelta

from django.utils import timezone


class BaseScoringService:

    FIRST_DAYS = 2  # how many days count as first days

    def get_dates(self):
        now = timezone.now()
        first_days_start = now - timedelta(days=self.FIRST_DAYS)
        first_week_start = \
            first_days_start - timedelta(days=7 - self.FIRST_DAYS)
        second_week_start = first_week_start - timedelta(days=7)
        third_week_start = second_week_start - timedelta(days=7)
        return {
            'now': now,
            'first_days_start': first_days_start,
            'first_week_start': first_week_start,
            'second_week_start': second_week_start,
            'third_week_start': third_week_start,
        }
