from django.conf.urls import patterns, url

from horsebook.booking.views import (
    create_booking,
    participate,
    student_abort_booking,
    show_booking,
    trainer_abort_booking_row,
    edit_booking
)

from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    url(r'^edit/(?P<booking_id>[0-9]+)', view=edit_booking),
    url(r'^show_booking/(?P<booking_id>[0-9]+)', view=show_booking),
    url(r'^student_abort/(?P<booking_id>[0-9]+)', view=student_abort_booking),
    url(r'^trainer_abort/(?P<booking_row_id>[0-9]+)', view=trainer_abort_booking_row),
    url(r'^create$', view=create_booking),
    url(r'^participate$', view=participate),
    url(r'^confirm', TemplateView.as_view(template_name="booking/confirm.html")),
    url(r'^confirm_participate', TemplateView.as_view(template_name="booking/confirm_participate.html")),
)
