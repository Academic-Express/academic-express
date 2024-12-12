# flake8: noqa
from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['*']

SECRET_KEY = env('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE', default='django.db.backends.mysql'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD').strip(),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'OPTIONS': env('DB_OPTIONS', cast=dict, default={
            'charset': 'utf8mb4'
        }),
    }
}

MEDIA_URL = env('MEDIA_URL', default='/media/')

FEED_ENGINE_URL = env('FEED_ENGINE_URL')
FEED_ENGINE_TOKEN = env('FEED_ENGINE_TOKEN').strip()
