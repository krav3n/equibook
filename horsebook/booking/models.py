# -*- coding: utf-8 -*-

# python std lib
from datetime import datetime

# django imports
from django.db import models
from django.utils import timezone

# horsebook imports
from horsebook.common.db.models import TimestampedModel
from horsebook.trainer.models import Trainer
from horsebook.student.models import Student

# 3rd party
from localflavor.se.forms import COUNTY_CHOICES


class Booking(TimestampedModel):
    """
    """

    # All dicipline key/value pairs should match TrainerDicipline when in dev & production
    DICIPLINE_DESSYR = 1
    DICIPLINE_HOPPNING = 2
    DICIPLINE_FALTTAVLAN = 3
    DICIPLINE_TOMKORNING = 4
    DICIPLINE_LOSHOPPNING = 5
    DICIPLINE_SADELUTPROVARE = 6
    DICIPLINE_AKADEMISK_RIDNING = 7
    DICIPLINE_WESTERN = 8
    DICIPLINE_WORKING_EQUITATION = 9

    DESSYR = u"Dressyr"
    HOPPNING = u"Hoppning"
    FALTTAVLAN = u"Fälttävlan"
    TOMKORNING = u"Tömkörning"
    LOSHOPPNING = u"Löshoppning"
    SADELUTPROVARE = u"Sadelutprovare"
    ADADEMISK_RIDNING = u"Akademisk Ridning"
    WESTERN = u"Western"
    WORKING_EQUITATION = u"Working Equitation"

    DICIPLINE_CHOICES = (
        (DICIPLINE_DESSYR, DESSYR),
        (DICIPLINE_HOPPNING, HOPPNING),
        (DICIPLINE_FALTTAVLAN, FALTTAVLAN),
        (DICIPLINE_TOMKORNING, TOMKORNING),
        (DICIPLINE_LOSHOPPNING, LOSHOPPNING),
        (DICIPLINE_SADELUTPROVARE, SADELUTPROVARE),
        (DICIPLINE_AKADEMISK_RIDNING, ADADEMISK_RIDNING),
        (DICIPLINE_WESTERN, WESTERN),
        (DICIPLINE_WORKING_EQUITATION, WORKING_EQUITATION),
    )
    DICIPLINES = [l[0] for l in DICIPLINE_CHOICES]
    DICIPLINES_MAP = {l[0]: l[1] for l in DICIPLINE_CHOICES}

    # Planning is when trainer have created it but it has not yet happened
    # Canceled can happen if the requirements was not meet or the trainer cacneled it
    # Done is a training that happened and it is past the 'at' date
    STATE_PLANNING = 1
    STATE_CANCELED = 2
    STATE_DONE = 3

    PLANNING = "planning"
    CANCELED = "canceled"
    DONE = "done"

    STATE_CHOICES = (
        (STATE_PLANNING, PLANNING),
        (STATE_CANCELED, CANCELED),
        (STATE_DONE, DONE),
    )

    STATES = [s[0] for s in STATE_CHOICES]
    STATUS_MAP = {s[0]: s[1] for s in STATE_CHOICES}

    # The user that created this booking
    trainer = models.ForeignKey(Trainer)

    # Time the practise should be held
    when = models.DateTimeField()

    # How long the training is planned to be
    duration = models.PositiveIntegerField(default=60)

    # This field should be used to determine if this booking have happened
    #  yet or not. Is it more efficient to bulk update it via cron rather
    #  then diffing time objects all the time.
    happened = models.BooleanField(default=False)

    dicipline = models.PositiveIntegerField(choices=DICIPLINE_CHOICES)

    # Basic location information required to define the place
    street = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    county = models.CharField(max_length=4, choices=COUNTY_CHOICES)
    club = models.CharField(max_length=255)

    # Notes by the trainer that can contain instructions etc
    notes = models.TextField(max_length=1000, verbose_name="Notes", blank=True)

    # This field will only be used if the booking was canceled
    canceled_notes = models.TextField(verbose_name="canceled notes", blank=True)

    price = models.PositiveIntegerField()

    # The maximum number of participants allowed for this booking
    max_participants = models.PositiveIntegerField(default=9)

    # Should be updated from BookingRow.save() to reduce number of queries
    # when looking up booking row statuses on a booking
    free_spots = models.PositiveIntegerField(default=9)

    state = models.PositiveIntegerField(choices=STATE_CHOICES, default=STATE_PLANNING)

    # Map coordinates
    lat = models.FloatField('Latitude', blank=True, null=True)
    lon = models.FloatField('Longitude', blank=True, null=True)
    trainer_set_coordinates = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(u"{0}  {1}  {2}".format(
            self.club, self.city, self.when,
        ))

    def clean(self):
        # TODO: Validate the number of participants is not yet reached
        return super(Booking, self).clean()

    def format_location(self):
        return u"{}, {}".format(self.street, self.city)

    def booking_full(self):
        """
        Returns if the booking is full or not
        """
        # 0 means that there can be any number of participants
        if self.max_participants == 0:
            return False

        # TODO: Validate this one more time

        # num_participants = len(self.bookingrow_set.filter(status__in=(
        #     BookingRow.STATUS_PAID, BookingRow.STATUS_NOT_PAID
        # )))

        # Check just for safty
        # if num_participants > self.max_participants:
        #     raise Exception("If this happens then there is a problem... There should not be possible to have more participants then max number of participants")

        return self.free_spots == 0

    def done(self):
        """
        Return boolean if this booking has been done or not
        """
        return self.state == self.STATE_DONE

    def canceled(self):
        """
        """
        return self.state == self.STATE_CANCELED

    def editable(self):
        """
        Determines if this booking is editable by the trainer
        """
        if timezone.make_aware(datetime.now(), timezone.get_default_timezone()) >= self.when:
            return False

    def booking_full_str(self):
        """
        Returns a Yes/No string if it is full or not
        """
        return "Yes" if self.booking_full() else "No"

    def good_booking_rows(self):
        """
        Return all objects that is considered confirmed or will be
        confirmed when payment has been done.
        """
        return self.bookingrow_set.filter(
            status__in=(BookingRow.STATUS_PAID, BookingRow.STATUS_NOT_PAID)
        )

    def num_spots_filled(self):
        return len(self.bookingrow_set.filter(
            status__in=(BookingRow.STATUS_PAID, BookingRow.STATUS_NOT_PAID)
        ))

    # def free_spots(self):
    #     """
    #     TODO: This method is expensive to calculate. Cache it...
    #     """
    #     return self.max_participants - self.num_spots_filled()

    def paid_participants(self):
        """
        Number of paid participants
        """
        return len(self.bookingrow_set.filter(status=BookingRow.STATUS_PAID))

    def not_paid_participants(self):
        """
        Number of not paid participants
        """
        return len(self.bookingrow_set.filter(status=BookingRow.STATUS_NOT_PAID))

    def refund_pending(self):
        """
        Number of refund pending
        """
        return len(self.bookingrow_set.filter(status=BookingRow.STATUS_REFUND_PENDING))

    def refunded(self):
        """
        Number of refunded rows
        """
        return len(self.bookingrow_set.filter(status=BookingRow.STATUS_REFUNDED))

    def status_string(self):
        """
        Return a string with the status
        """
        return self.STATUS_MAP[self.state]

    def calc_earned(self):
        """
        Returns the already earned money for this booking
        """
        return self.paid_participants() * self.price

    def calc_pending_earned(self):
        """
        This should calculate the payments that is incomming that is not yet confirmed
        """
        return self.not_paid_participants() * self.price

    def aborted(self):
        """
        Helper for templates to easily determine if a booking is canceled or not
        """
        return self.state in (self.STATE_CANCELED, )


class BookingRow(TimestampedModel):
    """
    This model is for each student that have made a booking on a specific Booking
    model instance. It should contain who did it and the payment status of it.
    """
    STATUS_NOT_PAID = 1
    STATUS_PAID = 2
    STATUS_REFUND_PENDING = 3
    STATUS_REFUNDED = 4

    NOT_PAID = "not paid"
    PAID = "paid"
    REFUND_PENDING = "refund pending"
    REFUNDED = "refunded"

    STATE_CHOICES = (
        (STATUS_NOT_PAID, NOT_PAID),
        (STATUS_PAID, PAID),
        (STATUS_REFUND_PENDING, REFUND_PENDING),
        (STATUS_REFUNDED, REFUNDED),
    )
    STATES = [s[0] for s in STATE_CHOICES]
    STATUS_MAP = {s[0]: s[1] for s in STATE_CHOICES}

    PAYMENT_STRIPE = 1

    STRIPE = "stripe"

    PAYMENT_CHOICES = (
        (PAYMENT_STRIPE, STRIPE),
    )
    PAYMENTS = [p[0] for p in PAYMENT_CHOICES]
    PAYMENT_MAP = {p[0]: p[1] for p in PAYMENT_CHOICES}

    payment = models.PositiveIntegerField(choices=PAYMENT_CHOICES, default=PAYMENT_STRIPE)
    student = models.ForeignKey(Student)
    booking = models.ForeignKey(Booking)
    status = models.PositiveIntegerField(choices=STATE_CHOICES, default=STATUS_NOT_PAID)
    abort_reason = models.TextField(verbose_name="Abort Reason", blank=True)

    def __unicode__(self):
        return unicode(self.id)

    def save(self, *args, **kwargs):
        """
        """
        # TODO: Update the bound self.booking with a new value for
        super(BookingRow, self).save(*args, **kwargs)

    def refund(self):
        """
        This code path should trigger the nessesary stuff that will make
        this booking row refund back the payment.
        """
        print("This will trigger a refund for booking row: {0}".format(self))

    def abortable(self):
        """
        Determines if this booking row is abortable by a trainer
        """
        # A row should not be refundable if the booking has happened or was canceled
        if self.booking.state in (Booking.STATE_CANCELED, Booking.STATE_DONE):
            return False

        return self.status in (self.STATUS_PAID, self.STATUS_NOT_PAID)

    def refundable(self):
        """
        Determines if this booking row is refundable
        """
        return self.status in (self.STATUS_PAID, )

    def is_aborted(self):
        """
        """
        return self.status in (self.STATUS_REFUNDED, self.STATUS_REFUND_PENDING)
