# support imports
from base import *

BASE_URL = 'localhost:8080'

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eqdev',
        'HOST': 'hb-mysql.docker',
        'PORT': '3306',
        'USER': "wq",
        'PASSWORD': "abcd",
    },
}

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',
)


MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

# If enabled the worker pool can be restarted using the pool_restart remote control command.
CELERYD_POOL_RESTARTS = True

STATIC_ROOT = "/tmp/static"


def show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': __name__ + '.show_toolbar',
}

SUIT_CONFIG = {
    'ADMIN_NAME': 'EquiBook',
    'MENU': (
        {'label': 'All Bookings', 'url': '/booking/booking', 'icon': 'icon-book'},
        {'label': 'All BookingRows', 'url': '/booking/bookingrow', 'icon': 'icon-list'},
        {'label': 'All Student', 'url': '/student/student', 'icon': 'icon-user'},
        {'label': 'All Trainers', 'url': '/trainer/trainer', 'icon': 'icon-user'},
        {'label': 'Search', 'url': '/search/search', 'icon': 'icon-search'},
    )
}

USE_L10N = True
USE_TZ = True
USE_I18N = True

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://elasticsearch.docker:9200',
        'INDEX_NAME': 'documents',
    },
}

# RabbitMQ server url and credentials
BROKER_URL = 'amqp://guest@hb-rabbitmq.docker:5672//'

cache_backend = 'django.core.cache.backends.memcached.MemcachedCache'
cache_location = 'hb-memcached.docker:11211'
CACHES = {
    'default': {
        'BACKEND': cache_backend,
        'LOCATION': cache_location,
        'KEY_PREFIX': 'default',
    }
}
