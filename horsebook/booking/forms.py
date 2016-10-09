# Create the form class.

from django import forms
from django.forms.widgets import HiddenInput

from datetimewidget.widgets import DateTimeWidget
from localflavor.se.forms import SEPostalCodeField, COUNTY_CHOICES

from horsebook.booking.models import Booking, BookingRow


class EditBookingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        assert self.request, 'request must be passed as a kwargs'
        super(EditBookingForm, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(EditBookingForm, self).clean()
        return data

    class Meta:
        model = Booking
        fields = [
            'when', 'street', 'zipcode',
            'county', 'city', 'max_participants', 'club', 'notes',
        ]


class CreateBookingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)

        assert self.request, 'request must be passed as a kwargs'

        super(CreateBookingForm, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        cleaned_data = super(CreateBookingForm, self).clean()

        # Bind the current user as the trainer of the booking
        cleaned_data["trainer"] = self.request.user
        return cleaned_data

    when = forms.DateTimeField(
        widget=DateTimeWidget(
            attrs={
                'weekStart': '1',
                'autoclose': 'false',
            },
            options={
                'startView': '2',
                'format': 'yyyy-dd-mm hh:ii',
                'showSeconds': 'false',
                'startDate': '0',
                'todayBtn': 'true',
                'todayHighlight': 'true',
                'minuteStep': '15',
                'maxView': '4',
            },
            usel10n=True,
            bootstrap_version=2,
        ),
        required=True,
        # TODO: This is a hack, it should hanel this by itself
        input_formats=[
            '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
            '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
            '%Y-%m-%d',              # '2006-10-25'
            '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
            '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
            '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
            '%m/%d/%y %H:%M',        # '10/25/06 14:30'
            '%m/%d/%Y',              # '10/25/2006'
            '%m/%d/%y',              # '10/25/06'
        ]
    )

    county = forms.ChoiceField(
        choices=COUNTY_CHOICES
    )

    city = forms.CharField()

    # Cleaned format will be XXXXX
    zipcode = SEPostalCodeField(required=True)

    price = forms.IntegerField(min_value=0, max_value=1000)

    max_participants = forms.IntegerField(min_value=0, max_value=20)

    class Meta:
        model = Booking
        fields = [
            'when', 'street', 'zipcode',
            'county', 'price', 'city',
            'max_participants', 'club', 'notes',
        ]


class ParticipateBookingForm(forms.ModelForm):
    """
    """

    payment = forms.ChoiceField(
        required=True,
        choices=BookingRow.PAYMENT_CHOICES,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        assert self.request, 'request must be passed as a kwargs'

        super(ParticipateBookingForm, self).__init__(*args, **kwargs)

        self.fields['booking'].widget = HiddenInput()
        self.fields['booking'].initial = self.request.GET.get("booking", None)

    def clean(self, *args, **kwargs):
        cleaned_data = super(ParticipateBookingForm, self).clean()
        return cleaned_data

    class Meta:
        model = BookingRow
        fields = [
            'payment', 'booking',
        ]


class StudentAbortForm(forms.ModelForm):
    """
    This form should handle when a student wants to abort
    a booking it has made. It should in the end trigger a refund
    of the paid ammount.
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        assert self.request, 'request must be passed as a kwargs'

        super(StudentAbortForm, self).__init__(*args, **kwargs)

        # self.fields['booking'].widget = HiddenInput()
        self.fields['booking'].initial = self.request.GET.get("id", None)

    def clean(self, *args, **kwargs):
        cleaned_data = super(StudentAbortForm, self).clean()
        return cleaned_data

    class Meta:
        model = BookingRow
        fields = [
            'abort_reason', 'booking', 'student',
            'payment', 'status',
        ]
