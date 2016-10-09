from django.conf.urls import patterns, url
from django.contrib.auth.views import logout

from horsebook.frontpage.views import (
    all_trainers,
    all_trainings,
    booking_map,
    booking_reserv,
    booking_students,
    cancel,
    cancel_trainer,
    do_login,
    edit_booking,
    faq,
    kontakt,
    login,
    newbooking,
    make_new_booking,
    payments,
    payment_details,
    profile,
    register,
    schema,
    settings,
    show,
    show_booking,
    team,
)
from django.views.generic.base import RedirectView


urlpatterns = patterns(
    '',
    url(r'^$', view=show),
    url(r'^trainer/', view=all_trainers),

    url(r'^booking/cancel_trainer/(?P<id>[0-9]+)', view=cancel_trainer),
    url(r'^booking/cancel_trainer', RedirectView.as_view(url='/booking', permanent=False), name='cancel_redirect'),

    url(r'^booking/cancel_student/(?P<id>[0-9]+)', view=cancel),
    url(r'^booking/cancel_student', RedirectView.as_view(url='/booking', permanent=False), name='cancel_redirect'),
    url(r'^booking/reserv/(?P<id>[0-9]+)', view=booking_reserv),
    url(r'^booking/reserv', RedirectView.as_view(url='/booking', permanent=False), name='reserv_redirect'),
    url(r'^booking/new', view=newbooking),
    url(r'^booking/make_new', view=make_new_booking),
    url(r'^booking/map/(?P<id>[0-9]+)', view=booking_map),
    url(r'^booking/map', RedirectView.as_view(url='/booking', permanent=False), name='map_redirect'),
    url(r'^booking/students/(?P<id>[0-9]+)', view=booking_students),
    url(r'^booking/students', RedirectView.as_view(url='/booking', permanent=False), name='students_redirect'),
    url(r'^booking/edit/(?P<id>[0-9]+)', view=edit_booking),
    url(r'^booking/(?P<id>[0-9]+)', view=show_booking),
    url(r'^booking', view=all_trainings),

    url(r'^profile/$', view=profile),
    url(r'^profile/(?P<id>[0-9]+)', view=profile),
    url(r'^profile/schema/(?P<id>[0-9]+)', view=schema),
    url(r'^profile/schema/', view=schema),
    url(r'^profile/payments', view=payments),
    url(r'^profile/payment/(?P<id>[0-9]+)', view=payment_details),
    url(r'^profile/payment', RedirectView.as_view(url='/booking', permanent=False), name='payment_redirect'),
    url(r'^profile/settings', view=settings),

    url(r'^faq', view=faq),
    url(r'^register', view=register),
    url(r'^login/skicka/$', view=do_login),
    url(r'^login$', view=login),
    url(r'^logout/$', logout, {'next_page': '/'}),
    url(r'^kontakt', view=kontakt),
    url(r'^team', view=team),
)
