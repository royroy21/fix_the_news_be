from celery import shared_task

from fix_the_news.news_items import models
from fix_the_news.news_items.services import scoring_service


@shared_task
def score_news_item(news_item_id):
    news_item = models.NewsItem.objects.get(id=news_item_id)
    news_item.score = scoring_service.NewsItemScoringService()\
        .get_score(news_item)['total_score']
    news_item.save()
