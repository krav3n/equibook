# coding=utf-8
from django.db.models.signals import post_save, pre_delete

from horsebook.booking.models import Booking
from horsebook.student.models import Student
from horsebook.trainer.models import Trainer


def _index(instances):
    from .tasks import add_to_index_queue, CannotQueue
    try:
        add_to_index_queue(instances=instances)
    except CannotQueue:
        pass


def index_trainer(sender, instance, **kwargs):
    """
    """
    print("Indexing trainer...")
    _index([instance])


def index_student(sender, instance, **kwargs):
    """
    """
    print("Indexing student...")
    _index([instance])


def index_booking(sender, instance, **kwargs):
    """
    Catches a signal sent to update category in the search index,
    collects all related objects, and adds tasks to indexing queue.

    :param sender:
        Model sending the signal, i.e. Category.
    :param instance:
        Category instance to be (re-)indexed.
    :return:
        None
    """
    _index([instance])


post_save.connect(index_booking, Booking)
pre_delete.connect(index_booking, Booking)

post_save.connect(index_booking, Trainer)
pre_delete.connect(index_booking, Trainer)

post_save.connect(index_booking, Student)
pre_delete.connect(index_booking, Student)
