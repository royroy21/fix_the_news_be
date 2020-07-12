import os

from celery import Celery

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
    # example usage:
    # "fix_the_news.users.tasks.create_avatar_thumbnail": {
    #     "queue": "create_avatar_thumbnail",
    # },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
