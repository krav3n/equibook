# coding=utf-8
from haystack import indexes

from horsebook.booking.models import Booking


class BookingIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    street = indexes.CharField(model_attr='street')
    zipcode = indexes.CharField(model_attr='zipcode')
    city = indexes.CharField(model_attr='city')
    county = indexes.CharField(model_attr='county')
    club = indexes.CharField(model_attr='club')
    price = indexes.IntegerField(model_attr='price')
    state = indexes.IntegerField()
    when = indexes.DateTimeField(model_attr='when')
    dicipline = indexes.IntegerField(model_attr='dicipline')
    free_spots = indexes.IntegerField(model_attr='free_spots')

    # Track if this booking is full of participants or not
    full = indexes.BooleanField(default=False)

    def prepare_state(self, obj):
        return Booking.objects.get(id=obj.id).state

    def prepare_full(self, obj):
        return Booking.objects.get(id=obj.id).booking_full()

    def get_model(self):
        return Booking
