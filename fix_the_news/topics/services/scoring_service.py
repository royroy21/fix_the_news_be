from django.db.models import Sum

from fix_the_news.core.services.scoring_service import BaseScoringService
from fix_the_news.comments import models as comments_models
from fix_the_news.news_items import models as news_items_models
from fix_the_news.topics import models


class TopicScoringService(BaseScoringService):

    FIRST_DAYS_MULTIPLIER = 2
    FIRST_WEEK_MULTIPLIER = 1

    def get_score(self, topic):
        news_items_score = self.get_score_for_news_items(topic)
        comments_score = self.get_score_for_comments(topic)
        return news_items_score + comments_score

    def get_score_for_news_items(self, topic):
        score = news_items_models\
            .NewsItem.objects\
            .filter(topic=topic)\
            .aggregate(Sum('score'))['score__sum']
        if score is None:
            return 0
        else:
            return score

    def get_score_for_comments(self, topic):
        dates = self.get_dates()
        first_days = comments_models.Comment.objects.filter(
            topic=topic,
            start_date=dates['first_days_start'],
            end_date=dates['now'],
        ).count()
        if first_days:
            first_days_score = first_days * self.FIRST_DAYS_MULTIPLIER
        else:
            first_days_score = 0

        first_week = comments_models.Comment.objects.filter(
            topic=topic,
            start_date=dates['first_week_start'],
            end_date=dates['first_days_start'],
        ).count()
        if first_week:
            first_week_score = first_week * self.FIRST_WEEK_MULTIPLIER
        else:
            first_week_score = 0

        return first_days_score + first_week_score

    def get_highest_score(self):
        """ Returns highest topic score """
        highest_scored_topic = models.Topic.objects.order_by('-score').first()
        if not highest_scored_topic:
            return 0
        else:
            return highest_scored_topic.score
