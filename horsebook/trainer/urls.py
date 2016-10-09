# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from horsebook.trainer.views import profile

urlpatterns = patterns(
    '',
    url(r'^profile/(?P<profile_id>[0-9]+)', view=profile),
)
