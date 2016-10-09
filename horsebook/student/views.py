# -*- coding: utf-8 -*-

from horsebook.common.account.decorators import student_required
from horsebook.booking.models import BookingRow

from django.shortcuts import render


@student_required
def upcomming_bookings(request):
    """
    Fetch all upcomming bookings that the student has booked and show
    the status of each booking, the payment status etc.
    """
    booking_rows = BookingRow.objects.filter(
        student=request.user.student
    )

    return render(request, 'student/upcomming_bookings.html', {'student_bookings': booking_rows})


def profile(request, profile_id):
    """
    """
    return render(request, 'student/profile.html', {})
