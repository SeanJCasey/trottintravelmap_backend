from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

BASE_URL = "http://127.0.0.1:8000"

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.local'
