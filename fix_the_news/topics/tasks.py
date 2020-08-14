from celery import shared_task

from fix_the_news.topics import models
from fix_the_news.topics.services import scoring_service


@shared_task
def score_topic(topic_id):
    topic = models.Topic.objects.get(id=topic_id)
    topic.score = scoring_service.TopicScoringService().get_score(topic)
    topic.save()
