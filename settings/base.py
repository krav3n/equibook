"""
Django settings for support project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
# python std lib
import os
import sys
from os.path import abspath, dirname

# django imports
from django.contrib import messages

# 3rd party import
from kombu import Exchange, Queue

PROJECT_PATH = dirname(dirname(abspath(__file__)))
BASE_DIR = os.path.dirname(__file__)
FSROOT = PROJECT_PATH + '/'

sys.path.append(dirname(PROJECT_PATH))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fadsjokfiuporqejkjpiewqofjqgfasfjiafweoj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

SITE_ID = 1

# Application definition

INSTALLED_APPS = (
    'suit',
    # Django default
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # External
    'haystack',
    'celery',
    'datetimewidget',
    'location_field',
    # Internal
    'horsebook',
    'horsebook.booking',
    'horsebook.common.account',
    'horsebook.common.db',
    'horsebook.frontpage',
    'horsebook.student',
    'horsebook.trainer',
    'horsebook.search',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'horsebook.urls'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# This shold be set in prod.py and dev.py
# STATIC_ROOT = ...

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(FSROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Template files
TEMPLATE_DIRS = [os.path.join(FSROOT, 'templates')]

# Define file paths to various files
BASE_TEMPLATE = "base.html"
REMOTE_TEMPLATE = "remote.html"

LOGIN_URL = "/"

# A tuple of callables that are used to populate the context in RequestContext.
# These callables take a request object as their argument
# and return a dictionary of items to be merged into the context.
#
# New in Django 1.4: The django.core.context_processors.tz
# context processor was added in this release.
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)

#######################
# RabbitMQ / celery / django-celery settings

# For more details check the following pages;
#
#   https://pypi.python.org/pypi/django-celery/3.0.17
#   http://celery.readthedocs.org/en/3.0/configuration.html
#
# when reading the documentation, make sure you are on the
#   same version as the django-/celery packages we have installed!

# don't store task return results.
#
# this is something which we might want to change in the future,
#   although Redis would be a better backend store in such case.
CELERY_IGNORE_RESULT = True

# run celery tasks in async mode
CELERY_ALWAYS_EAGER = False

# define all our queues
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
)

# define routes for tasks that should use a specific queue
CELERY_ROUTES = ({})

# default queue to use,
#   in case task isn't routed to a specific queue.
CELERY_DEFAULT_QUEUE = 'default'

# RabbitMQ / celery / django-celery settings
#######################

# Control if requests should do ssl cert verification when running requests get/posts
SSL_VERIFY = False

# Name of our django-admin sites used by staff.
BASE_SITE_NAME = 'staff'

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

TRAINER_LOGIN_URL = "/login/"
STUDENT_LOGIN_URL = "/login/"

##################
# Django admin bootstrapped config

MESSAGE_TAGS = {
    messages.SUCCESS: 'alert-success success',
    messages.WARNING: 'alert-warning warning',
    messages.ERROR: 'alert-danger error'
}

USE_TZ = True
