# coding: utf-8

"""
Celery tasks for indexing updated models.
"""
import logging
import socket

from horsebook.celeryd import app

from haystack import connections
from haystack.utils import get_identifier

from django.core.cache import get_cache
from django.db.models import get_model

# TODO: setup separate cache for indexing
cache = get_cache('default')

DISABLED_TOKEN = 'TEMP_DISABLED'


class CannotQueue(Exception):
    pass


def add_to_index_queue(instances):
    """
    A general function for queuing indexing with locking and too-early-request workaround.

    If running tests then run all indexing tasks in synchronous mode to avoid
     issues when a task is runned it expects a database with a certain setup of
     objects that may or may not be there when the task is runned in async mode.

    :param instances:
        Instances to be (re-)indexed.
    :return:
        None
    """
    if cache.get('indexqueue/{0}'.format(DISABLED_TOKEN)):
        # In case there is a problem connecting to the queue, this token
        # indicates that. If there is a problem connecting to the queue,
        # that will severely delay any operation that calls this function,
        # and since indexing operations aren't critical we want to simply
        # skip them in that case so that the application can continue to
        # function by just catching this exception.
        raise CannotQueue()

    if not hasattr(instances, '__iter__'):
        instances = [instances]

    for instance in instances:
        identifier = get_identifier(instance)

        # Post save signal is triggered before the transaction is
        # committed. Idle workers may try to fetch the db object
        # before it's saved. "Solved" with a countdown.
        # https://code.djangoproject.com/ticket/14051

        try:
            index_instance.apply_async(args=[identifier], countdown=2)
        except socket.error as e:
            # if settings.TEST_MODE:
            #     raise e

            # In case we can't connect to the queue, place a token in the
            # cache so that future calls to this function doesn't try to
            # connect, since this will severely delay any operation.
            cache.set('indexqueue/{0}'.format(DISABLED_TOKEN), True, 300)
            raise CannotQueue(str(e))


@app.task
def index_instance(identifier, using='default'):
    """
    Celery task for indexing model instances.

    :param identifier: Object identifier in haystack format (e.g. product.product.123)
    :param using: Current haystack connection name.
    :return: None
    """
    unified_index = connections[using].get_unified_index()
    backend = connections[using].get_backend()
    app_label, model_name, model_id = identifier.split('.', 2)
    model = get_model(app_label, model_name)
    index = unified_index.get_index(model)

    try:
        queryset = index.index_queryset().filter(id=model_id)
        if queryset.exists():
            # WARNING: check solrconfig.xml before changing to commit=False
            backend.update(index, queryset, commit=True)
    except Exception as e:
        logging.getLogger('default').exception("Indexing %s #%s failed: %r", model_name, model_id, e)
        raise e
