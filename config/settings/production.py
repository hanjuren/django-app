from .base import *
import environ
import os

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env.prod"))

SECRET_KEY = env("SECRET_KEY")

JWT_SECRET_KEY = env('JWT_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = []

AWS_STORAGE_BUCKET_NAME = 'hjr-django-development'
AWS_S3_ACCESS_KEY_ID = env('AWS_S3_ACCESS_KEY_ID')
AWS_S3_SECRET_ACCESS_KEY = env('AWS_S3_SECRET_ACCESS_KEY')

