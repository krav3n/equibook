from django.conf.urls import patterns, url

from horsebook.student.views import upcomming_bookings, profile

urlpatterns = patterns(
    '',
    url(r'^upcomming_bookings', view=upcomming_bookings),
    url(r'^profile/(?P<profile_id>[0-9]+)', view=profile),
)
