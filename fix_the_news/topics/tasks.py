from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone

from fix_the_news.topics import models
from fix_the_news.topics.services import scoring_service


logger = get_task_logger(__name__)


@shared_task
def score_topic(topic_id):
    topic = models.Topic.objects.get(id=topic_id)
    topic.score = scoring_service.TopicScoringService().get_score(topic)
    topic.save()


@shared_task
def score_all_topics():
    start = timezone.now()
    # TODO - Find a solution to remove topics without activity
    topics = models.Topic.objects.all()
    for topic in topics:
        topic.score = scoring_service.TopicScoringService().get_score(topic)
        topic.save()
    finish = timezone.now()
    time_taken = finish - start
    logger.info(f'finished score_all_topics task in '
                f'{time_taken.total_seconds()} seconds')
