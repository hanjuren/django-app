import environ
from .base import *

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env.prod"))

SECRET_KEY = env("SECRET_KEY")
DEBUG = True
ALLOWED_HOSTS = ['*']
