import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    f"fix_the_news.{os.environ['DJANGO_SETTINGS_MODULE']}",
)

app = Celery("fix_the_news")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.task_routes = {
    "fix_the_news.news_items.tasks.score_all_news_items": {
        "queue": "scoring",
    },
    "fix_the_news.topics.tasks.score_all_topics": {
        "queue": "scoring",
    },
}

beat_schedule = {
    task: settings.AVAILABLE_BEAT_SCHEDULES[task]
    for task
    in settings.ENABLED_BEAT_SCHEDULES
}
app.conf.beat_schedule = beat_schedule
app.conf.timezone = "Europe/London"

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
