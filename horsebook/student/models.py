# coding=utf-8

from django.db import models
from django.contrib.auth.models import User

from horsebook.common.db.models import TimestampedModel


class Student(TimestampedModel):
    user = models.OneToOneField(User, related_name='student')

    name = models.CharField(verbose_name='student name', max_length=255, db_index=True)
    phone = models.CharField(verbose_name='student phone support', max_length=32)
    email = models.CharField(verbose_name='student email', max_length=32)

    # A short summary of the user
    bio = models.CharField(verbose_name='biography', max_length=500)

    class Meta:
        verbose_name = 'student'
        verbose_name_plural = 'student'
        permissions = ()

    def __unicode__(self):
        return self.name
