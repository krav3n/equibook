# coding=utf-8

from django.db import models


class TimestampedModel(models.Model):
    """
    Simple helper model that implemented automatic created & updated fields
    """
    created = models.DateTimeField(verbose_name='created', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='changed', auto_now=True)

    class Meta:
        abstract = True
