import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

sentry_key = os.environ['SENTRY_KEY']
sentry_org = os.environ['SENTRY_ORGANISATION']
sentry_project = os.environ['SENTRY_PROJECT']
sentry_sdk.init(
    dsn=f"https://{sentry_key}@{sentry_org}.ingest.sentry.io/{sentry_project}",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = True if os.environ["DEBUG"] == "True" else False

ALLOWED_HOSTS = [
    os.environ["DJANGO_HOST"],
]

CORS_ORIGIN_WHITELIST = (
    f"http://{os.environ['WEB_APP_HOST']}",
    f"https://{os.environ['WEB_APP_HOST']}",
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ["DATABASE_NAME"],
        'USER': os.environ["DATABASE_USER"],
        'PASSWORD': os.environ["DATABASE_PASSWORD"],
        'HOST': os.environ["DATABASE_HOST"],
        'PORT': os.environ["DATABASE_PORT"],
    }
}

# TODO - media to be stored on s3 bucket ?
STATIC_ROOT = '/app/static'
MEDIA_ROOT = '/app/media'
