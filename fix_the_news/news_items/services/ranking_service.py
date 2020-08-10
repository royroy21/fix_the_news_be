from datetime import datetime, timedelta

from fix_the_news.likes import models as likes_models
from fix_the_news.views import models as views_models


# TODO -
# 1) Need a way to have newly created news items have a higher score
#    than any others in it's first few hours so it has a chance to be seen by
#    users.
# 2) Will need some kind of task to remove this generous first created score.
# 3) Need a rabbit task to run every few hours to update scores
# 4) Need to decide on a how to not score really old news items than haven't
#    any activity for a while. This is important - we need to keep the update
#    task to run as fast as possible.
class NewsItemRankingService:
    """
    This ranks a news item by calculating a score for the first few days,
    the first week, second week, third week and finally the rest of time it
    has existed.

    Scoring is based upon how many likes and views a news item collects.

    Scoring is weighted so that likes and views are worth more the earlier
    they are created. For example likes and views in the first week would
    be scored using a much higher multiplier in the first week than the
    forth week. This is so news items will score less over time unless
    they keep acquiring more likes and views.
    """

    FIRST_DAYS = 2  # how many days count as first days

    FIRST_DAYS_MULTIPLIER = 10
    FIRST_WEEK_MULTIPLIER = 5
    SECOND_WEEK_MULTIPLIER = 3
    THIRD_WEEK_MULTIPLIER = 2

    LIKES_MULTIPLIER = 4
    VIEWS_MULTIPLIER = 1

    def get_total_score(self, news_item):
        now = datetime.now()
        first_days_start = now - timedelta(days=2)
        first_days_score = self.calculate_score_for_time_period(
            news_item=news_item,
            multiplier=self.FIRST_DAYS_MULTIPLIER,
            start_date=first_days_start,
            end_date=now,
        )
        first_week_start = first_days_start - timedelta(days=5)
        first_week_score = self.calculate_score_for_time_period(
            news_item=news_item,
            multiplier=self.FIRST_WEEK_MULTIPLIER,
            start_date=first_week_start,
            end_date=first_days_start,
        )
        second_week_start = first_week_start - timedelta(days=7)
        second_week_score = self.calculate_score_for_time_period(
            news_item=news_item,
            multiplier=self.SECOND_WEEK_MULTIPLIER,
            start_date=second_week_start,
            end_date=first_week_start,
        )
        third_week_start = second_week_start - timedelta(days=7)
        third_week_score = self.calculate_score_for_time_period(
            news_item=news_item,
            multiplier=self.THIRD_WEEK_MULTIPLIER,
            start_date=third_week_start,
            end_date=second_week_start,
        )
        the_rest_score = self.calculate_score_for_time_period(
            news_item=news_item,
            multiplier=1,
            start_date=third_week_start,
        )

        total_score = (
            first_days_score['total_score']
            + first_week_score['total_score']
            + second_week_score['total_score']
            + third_week_score['total_score']
            + the_rest_score['total_score']
        )
        return {
            'first_days_score': first_days_score,
            'first_week_score': first_week_score,
            'second_week_score': second_week_score,
            'third_week_score': third_week_score,
            'the_rest_score': the_rest_score,
            'total_score': total_score,
        }

    def calculate_score_for_time_period(
            self, news_item, multiplier, start_date, end_date=None):
        likes_score = self.calculate_score_for_model(
            model=likes_models.Like,
            news_item=news_item,
            multiplier=self.LIKES_MULTIPLIER,
            start_date=start_date,
            end_date=end_date,
        )
        views_score = self.calculate_score_for_model(
            model=views_models.View,
            news_item=news_item,
            multiplier=self.VIEWS_MULTIPLIER,
            start_date=start_date,
            end_date=end_date,
        )
        if likes_score or views_score:
            return {
                'likes_score': likes_score,
                'views_score': views_score,
                'multiplier': multiplier,
                'total_score': (likes_score + views_score) * multiplier,
            }
        else:
            return {
                'likes_score': likes_score,
                'views_score': views_score,
                'multiplier': multiplier,
                'total_score': 0,
            }

    def calculate_score_for_model(
            self, model, news_item, multiplier, start_date, end_date=None):
        args = {
            'news_item': news_item,
            'date_created__gte': start_date,
        }
        if end_date:
            args['date_created__lte'] = end_date

        query = model.objects.filter(**args)
        if query:
            return query.count() * multiplier
        else:
            return 0