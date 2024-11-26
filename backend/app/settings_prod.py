import os
from pathlib import Path

from .settings import *  # noqa: F403, F401

DEBUG = False

ALLOWED_HOSTS = ['*']

SECRET_KEY = Path(os.environ['SECRET_KEY_FILE']).read_text().strip()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': Path(os.environ['DB_PASSWORD_FILE']).read_text().strip(),
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
    }
}

MEDIA_URL = '/media/'

FEED_ENGINE_URL = os.environ['FEED_ENGINE_URL']
FEED_ENGINE_TOKEN = Path(os.environ['FEED_ENGINE_TOKEN_FILE']).read_text().strip()
