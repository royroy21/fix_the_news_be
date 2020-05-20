from .base import *

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
