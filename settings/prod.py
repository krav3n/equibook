# Import all base settings
from base import *

DEBUG = False
TEMPLATE_DEBUG = False

# Production settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev_database',
    }
}

STATIC_ROOT = "/srv/www/horsebook/static"

# RabbitMQ server url and credentials
BROKER_URL = 'amqp://guest@127.0.0.1:5672//'

cache_backend = 'django.core.cache.backends.memcached.MemcachedCache'
cache_location = 'hb-memcached.docker:11211'
CACHES = {
    'default': {
        'BACKEND': cache_backend,
        'LOCATION': cache_location,
        'KEY_PREFIX': 'default',
    }
}
