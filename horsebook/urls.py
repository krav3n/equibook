# django imports
from django.conf.urls import patterns, include, url
from django.contrib import admin

import horsebook.frontpage.urls as frontpage_urls
import horsebook.trainer.urls as trainer_urls
import horsebook.student.urls as student_urls
import horsebook.booking.urls as booking_urls
import horsebook.search.urls as search_urls
from horsebook.site import site

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Frontpage
    url(r'^', include(frontpage_urls)),
    # url(r'^trainer/', include(trainer_urls)),
    # url(r'^student/', include(student_urls)),
    # url(r'^booking/', include(booking_urls)),
    # url(r'^search/', include(search_urls)),
    # url(r'^', include(site.urls)),

    # Backend dev admin
    # url(r'^adminz0r/', include(admin.site.urls)),
)
