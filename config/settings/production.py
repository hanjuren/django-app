from .base import *
import environ
import os

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env.prod"))

SECRET_KEY = env("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = []
