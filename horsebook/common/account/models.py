# coding=utf-8

# import datetime
# from logging import debug

# from django.db import models
# from django.conf import settings
# from django.contrib.auth.models import (
#     BaseUserManager, AbstractBaseUser
# )


# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
#     phone = models.CharField(max_length=32, blank=True, null=True)

#     class Meta:
#         permissions = (
#             ('can_impersonate', 'Can log in as merchant'),
#             ('can_change_product_proposal_step', 'Can allow/forbid skipping product proposal step'),
#             ('payment_create', 'Can create payments'),
#             ('change_bank_accounts', 'Can change bank account'),
#             ('can_block_and_unblock', 'Can block / unblock'),
#         )

#     def __unicode__(self):
#         return unicode(self.user)

#     def is_complete(self):
#         if self.user.first_name is None or len(self.user.first_name) < 2:
#             debug("firstname not complete")
#             return False
#         if self.user.last_name is None or len(self.user.last_name) < 2:
#             debug("lastname not complete")
#             return False
#         if self.user.email is None or len(self.user.email) < 3:
#             debug("email not complete")
#             return False
#         if self.phone is None or len(self.phone) < 5:
#             debug("phone not complete")
#             return False
#         return True


# class MyUserManager(BaseUserManager):
#     def create_user(self, email, date_of_birth, password=None):
#         """
#         Creates and saves a User with the given email, date of
#         birth and password.
#         """
#         if not email:
#             raise ValueError('Users must have an email address')

#         user = self.model(
#             email=self.normalize_email(email),
#             date_of_birth=date_of_birth,
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, date_of_birth, password):
#         """
#         Creates and saves a superuser with the given email, date of
#         birth and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#             date_of_birth=date_of_birth,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user


# class MyUser(AbstractBaseUser):
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True,
#     )
#     # date_of_birth = models.DateField()
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=True)

#     objects = MyUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def get_full_name(self):
#         # The user is identified by their email address
#         return self.email

#     def get_short_name(self):
#         # The user is identified by their email address
#         return self.email

#     def __str__(self):              # __unicode__ on Python 2
#         return self.email

#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True

#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True

#     # @property
#     # def is_staff(self):
#     #     "Is the user a member of staff?"
#     #     # Simplest possible answer: All admins are staff
#     #     return self.is_admin

import random
import string
from django.db import models

from django.contrib.auth.models import User
from django.db.models.loading import get_model


DEFAULT_ALPHABET = string.ascii_letters + string.digits


def generate_unsafe_token(DbObject=None, field_name=None,
                          alphabet=DEFAULT_ALPHABET, length=16, prefix=None):
    """
    Generates a pseudo random token suitable for use in non-critical applicaitons.
    """
    if isinstance(DbObject, str):
        try:
            DbObject = get_model(*(DbObject.split('.', 1)))
        except:
            DbObject = None

    if DbObject and field_name:
        not_unique = True
        fail_counter = 0
        while not_unique:
            if prefix:
                code = prefix + ''.join([random.choice(alphabet) for x in xrange(length - len(prefix))])
            else:
                code = ''.join([random.choice(alphabet) for x in xrange(length)])
            try:
                DbObject.objects.get(**{field_name: code})
            except DbObject.DoesNotExist:
                not_unique = False

                if fail_counter > 1000:
                    raise ValueError('Failed to generate unique token.')
                fail_counter += 1
        return code
    elif DbObject or field_name:
        raise ValueError('Both DbObject and field_name must be set for uniqueness check to work.')
    else:
        return ''.join([random.choice(alphabet) for x in xrange(length)])


def default_token(obj_str, field_name):
    return lambda: generate_unsafe_token(
        DbObject=obj_str, field_name=field_name,
        alphabet=string.ascii_lowercase+string.digits, length=20)


class PasswordReset(models.Model):
    created_at = models.DateTimeField()
    valid_until = models.DateTimeField()
    token = models.CharField(max_length=20, default=default_token('account.PasswordReset', 'token'))
    user = models.ForeignKey(User)
