# -*- coding: utf-8 -*-

from horsebook.admin import StaffAdmin
from horsebook.site import site
from horsebook.booking.models import Booking, BookingRow


class BookingAdmin(StaffAdmin):
    actions = []
    list_display = (
        'trainer', 'when', 'street',
        'zipcode', 'city', 'county',
        'club', 'price', 'max_participants',
        'paid_participans', 'not_paid_participans', 'refund_pending', 'refunded',
        'state', 'participate', 'created', 'updated',
        'happened', 'is_participant', 'booking_full',
    )
    list_filter = []
    list_max_show_all = 25
    list_per_page = 25
    search_fields = []

    def __init__(self, *args, **kwargs):
        super(BookingAdmin, self).__init__(*args, **kwargs)

    def queryset(self, request):
        """
        For super users show all items.
        If trainer then show all bookings that belongs to that person.
        A student should see all
        """
        self.request = request

        q = super(BookingAdmin, self).queryset(request)

        if hasattr(request.user, "trainer"):
            q = q.filter(trainer=request.user.trainer)

        return q

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def paid_participans(self, booking):
        return booking.paid_participants()
    paid_participans.short_description = u"paid participants"

    def not_paid_participans(self, booking):
        return booking.not_paid_participants()
    not_paid_participans.short_description = u"not paid participants"

    def refund_pending(self, booking):
        return booking.refund_pending()
    refund_pending.short_description = u'refund pending'

    def refunded(self, booking):
        return booking.refunded()
    refund_pending.short_description = u'refund pending'

    def participate(self, booking):
        return '<a href="/booking/participate?booking={0}">Participate</a>'.format(booking.id)
    participate.short_description = u"Participate"
    participate.allow_tags = True

    def is_participant(self, booking):
        if hasattr(self.request.user, 'student'):
            b = BookingRow.objects.filter(booking=booking.id, student=self.request.user.student).first()
            return "yes" if b else "no"
        else:
            return "---"
    is_participant.short_description = u'Is Participant'

    def booking_full(self, booking):
        return booking.booking_full()
    booking_full.short_description = u'Booking is full'


class BookingRowAdmin(StaffAdmin):
    actions = []
    list_display = ('student', 'booking', 'status', 'created', 'updated', 'abort_reason')
    list_filter = []
    list_max_show_all = 25
    list_per_page = 25
    search_fields = []

    def __init__(self, *args, **kwargs):
        super(BookingRowAdmin, self).__init__(*args, **kwargs)

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


# Register admin on main site
site.register(Booking, BookingAdmin)
site.register(BookingRow, BookingRowAdmin)
