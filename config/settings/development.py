from .base import *
import environ
import os

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env.dev"))

SECRET_KEY = env("SECRET_KEY")

JWT_SECRET_KEY = env('JWT_SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jr_development',
        'USER': env("POSTGRES_USER"),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': 'django_database',
        'PORT': '5432',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}
