from .base import *

CORS_ORIGIN_WHITELIST = (
    os.environ["WEB_APP_URL"],
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
