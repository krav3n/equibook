# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

from horsebook.common.account.decorators import student_required, trainer_required
from horsebook.booking.models import Booking, BookingRow
from horsebook.booking.forms import (
    CreateBookingForm,
    EditBookingForm,
    ParticipateBookingForm,
    StudentAbortForm,
)


def trainer_abort_booking_row(request, booking_row_id):
    """
    """
    pass


@csrf_protect
@student_required
def student_abort_booking(request, booking_id):
    """
    Only student can use this endpoint to abort its own booking row.
    """
    row = BookingRow.objects.filter(booking=booking_id, student=request.user.student).first()
    if not row:
        messages.error(request, 'No booking with that id was found in database')
        return redirect('/student/upcomming_bookings')

    if request.method == 'POST':
        # Student have filled out the abort form, validate it and
        #  then save it in database.
        form = StudentAbortForm(request.POST, request=request, instance=row)
        if form.is_valid():
            b = form.save(commit=False)
            b.status = BookingRow.STATUS_REFUND_PENDING
            b.save()

            # TODO: Trigger refunding code path...
            # b.refund()

            messages.info(request, 'Booking has been aborted and your payment will be refuned soon')
            return HttpResponseRedirect('/student/upcomming_bookings')
    else:
        form = StudentAbortForm(request=request, instance=row)

    return render(request, 'booking/student_abort.html', {'form': form})


@trainer_required
def edit_booking(request, booking_id):
    """
    Special form only for editing a booking.
    """
    booking = Booking.objects.get(pk=booking_id)
    if not booking:
        messages.error(request, 'No booking with that booking id was found in database')
        return redirect('/booking/booking')

    if booking.trainer != request.user.trainer:
        messages.error(request, 'That booking do not belong to you')
        return redirect('/booking/booking')

    if request.method == 'POST':
        form = EditBookingForm(request.POST, request=request, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.save()

            messages.info(request, 'Booking has been updated')
            return redirect('/trainer/profile/' + request.user.trainer.id)
    else:
        form = EditBookingForm(request=request, instance=booking)

    return render(request, 'booking/edit_booking.html', {'form': form})


@csrf_protect
@trainer_required
def create_booking(request):
    """
    Only a trainer can create a new Booking
    """
    if request.method == 'POST':
        form = CreateBookingForm(request.POST, request=request)
        if form.is_valid():
            return HttpResponseRedirect('/booking/confirm')
    else:
        form = CreateBookingForm(request=request)

    return render(request, 'booking/create.html', {'form': form})


@csrf_protect
@student_required
def participate(request):
    """
    Only a student should be able to view this form because they are the only one
    that can make a BookingRow
    """
    if request.method == 'POST':
        form = ParticipateBookingForm(
            request.POST,
            request=request,
        )

        if form.is_valid():
            b = form.save(commit=False)
            b.student = request.user.student
            b.save()

            return HttpResponseRedirect('/booking/confirm_participate')
    else:
        b_id = request.GET.get("booking", None)
        if not b_id:
            raise Exception("Missing required get parameter 'booking'")

        booking = Booking.objects.filter(id=b_id).first()
        if not booking:
            raise Exception("No booking with that id found")

        if booking.state == Booking.STATE_CANCELED:
            messages.error(request, 'That booking is canceled and can\' be joined')
            return HttpResponseRedirect('/booking/booking/')

        if timezone.make_aware(datetime.now(), timezone.get_default_timezone()) >= booking.when:
            return render(request, 'booking/booking_expired.html')

        if booking.booking_full():
            return render(request, 'booking/booking_full.html')

        # Check if you already is a participant of this booking
        if len(booking.bookingrow_set.filter(student=request.user.student)) > 0:
            return render(request, 'booking/already_participant.html')

        form = ParticipateBookingForm(request=request)

    return render(request, 'booking/participate.html', {'form': form})


def show_booking(request, booking_id):
    """
    Show more details for one booking
    """
    booking = Booking.objects.filter(id=booking_id).first()
    return render(request, 'booking/show_booking.html', {'booking': booking})
