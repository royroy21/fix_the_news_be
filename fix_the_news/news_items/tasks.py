from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone

from fix_the_news.news_items import models
from fix_the_news.news_items.services import scoring_service


logger = get_task_logger(__name__)


@shared_task
def score_news_item(news_item_id):
    news_item = models.NewsItem.objects.get(id=news_item_id)
    news_item.score = scoring_service.NewsItemScoringService()\
        .get_score(news_item)['total_score']
    news_item.save()


@shared_task
def score_all_news_items():
    start = timezone.now()
    # TODO - Find a solution to remove news items without activity
    news_items = models.NewsItem.objects.all()
    for news_item in news_items:
        news_item.score = scoring_service.NewsItemScoringService()\
            .get_score(news_item)['total_score']
        news_item.save()
    finish = timezone.now()
    time_taken = finish - start
    logger.info(f'finished score_all_news_items task in '
                f'{time_taken.total_seconds()} seconds')
