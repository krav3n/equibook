# coding=utf-8
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings

from horsebook.student.models import Student
from horsebook.trainer.models import Trainer


def user_access(user):
    """
    Checks if the user is authenticated, active and is either a student or trainer
    """
    # TODO: Fix this
    return True


def student_access(user):
    if user.is_authenticated() and user.is_active:
        try:
            getattr(user, 'student')
            return True
        except Student.DoesNotExist:
            return False
    return False


def student_required(function, login_url=None):
    """
    Forbids access to a view or function if doesn't have student_access permissions.
    """
    decorator = user_passes_test(
        student_access,
        login_url=login_url or settings.STUDENT_LOGIN_URL,  # TODO: These points to wrong url
    )
    if function:
        return decorator(function)
    return decorator


def trainer_access(user):
    if user.is_authenticated() and user.is_active:
        try:
            getattr(user, 'trainer')
            return True
        except Trainer.DoesNotExist:
            return False
    return False


def trainer_required(function, login_url=None):
    """
    Forbids access to a view or function if doesn't have trainer_access permissions.
    """
    decorator = user_passes_test(
        trainer_access,
        login_url=login_url or settings.TRAINER_LOGIN_URL,  # TODO: These points to wrong url
    )
    if function:
        return decorator(function)
    return decorator
