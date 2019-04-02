from .base import *

import dj_database_url


DEBUG = False
if os.environ.get('DEBUG', 'false').lower() == 'true':
    DEBUG = True

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

ALLOWED_HOSTS = ['trottintravelmap-backend.herokuapp.com']

# BASE_URL = 'https://trottintravelmap-backend.herokuapp.com'

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
