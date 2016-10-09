# -*- coding: utf-8 -*-

from django.shortcuts import render

from horsebook.trainer.models import Trainer
from horsebook.booking.models import Booking


def profile(request, profile_id):
    """
    """
    trainer = Trainer.objects.filter(id=profile_id).first()
    if not trainer:
        # TODO: Give 404 error or something
        pass

    bookings = Booking.objects.filter(trainer=trainer)

    return render(request, 'trainer/profile.html', {'bookings': bookings, 'trainer': trainer})
