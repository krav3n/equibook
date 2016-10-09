# coding=utf-8

# django imports
from django import forms
from django.forms import ModelForm, Textarea
from django.forms.widgets import Select
from horsebook.booking.models import Booking


dicipline_choices = (
    ('1', 'Dressyr'),
    ('2', 'Hoppning'),
    ('3', 'Fälttävlan'),
    ('4', 'Tömkörning'),
    ('5', 'Löshoppning'),
    ('6', 'Sadelutprovare'),
    ('7', 'Akademisk Ridning'),
    ('8', 'Western'),
    ('9', 'Working Equitation'),
)

distrikt_choices = (
    ('K',  'Blekinge'),
    ('W',  'Dalarna'),
    ('I',  'Gotland'),
    ('X',  'Gävleborg'),
    ('N',  'Halland'),
    ('Z',  'Jämtland'),
    ('F',  'Jönköping'),
    ('H',  'Kalmar'),
    ('G',  'Kronoberg'),
    ('BD', 'Norrbotten'),
    ('M',  'Skåne'),
    ('AB', 'Stockholm'),
    ('D',  'Södermaland'),
    ('C',  'Uppsala'),
    ('S',  'Värmland'),
    ('AC', 'Västerbotten'),
    ('Y',  'Västernorrland'),
    ('U',  'Västmaland'),
    ('O',  'Västra'),
    ('T',  'Örebro'),
    ('E',  'Östergötland'),
)

level_choices = (
    ('1', 'A-tränare'),
    ('2', 'B-tränare'),
    ('3', 'C-tränare'),
    ('4', 'Aspirant A'),
    ('5', 'Aspirant B'),
    ('6', 'Aspirant C'),
    ('7', 'Dressyr'),
    ('8', 'Inverkansdommare'),
    ('9', 'A - enbart'),
    ('10', 'B - enbart'),
    ('11', 'Master'),
)

booking_ordering_choices = (
    ('A', 'Datum'),
    ('B', 'Lediga platser'),
    ('C', 'Bokade platser'),
    ('D', 'Dyrast'),
    ('E', 'Billigast'),
)

duration_choices = (
    ('15', '15'),
    ('30', '30'),
    ('45', '45'),
    ('60', '60'),
    ('75', '75'),
    ('90', '90'),
    ('105', '105'),
    ('120', '120'),
)


class DefaultChoiceField(forms.ChoiceField):
    """
    Copied from: https://stackoverflow.com/questions/5522339/showing-please-choose-in-a-djangos-select-widget
    """

    def __init__(self, *args, **kwargs):
        self.blank_choice = kwargs.pop('blank_choice', None)
        self.blank_choice_value = kwargs.pop('blank_choice_value', None)
        super(DefaultChoiceField, self).__init__(*args, **kwargs)

    def _get_choices(self):
        return self._choices

    def _set_choices(self, value):
        choices = list(value)
        if self.blank_choice:
            choices = [(self.blank_choice_value, self.blank_choice)] + choices
        self._choices = self.widget.choices = choices

    choices = property(_get_choices, _set_choices)


class ProfileSearchForm(forms.Form):
    q = forms.CharField(max_length=128, required=False)
    county = DefaultChoiceField(choices=distrikt_choices, blank_choice='* Alla distrikt', blank_choice_value=0, required=False)
    level = DefaultChoiceField(choices=level_choices, blank_choice='* Alla Nivåer', blank_choice_value=0, required=False)
    dicipline = DefaultChoiceField(choices=dicipline_choices, blank_choice='* Alla dicipliner', blank_choice_value=0, required=False)
    page = forms.IntegerField(required=False)


class BookingSearchForm(forms.Form):
    q = forms.CharField(max_length=128, required=False)
    county = DefaultChoiceField(choices=distrikt_choices, blank_choice='* Alla distrikt', blank_choice_value=0, required=False)
    dicipline = DefaultChoiceField(choices=dicipline_choices, blank_choice='* Alla dicipliner', blank_choice_value=0, required=False)
    max_price = forms.IntegerField(required=False)
    ordering = DefaultChoiceField(choices=booking_ordering_choices, blank_choice='* Sortera på', blank_choice_value='', required=False)
    show_full_boked = forms.BooleanField(required=False)
    show_canceled = forms.BooleanField(required=False)
    show_done = forms.BooleanField(required=False)
    page = forms.IntegerField(required=False)


class FirstPageForm(forms.Form):
    county = DefaultChoiceField(widget=Select(attrs={'id': 'frontpage_county'}), choices=distrikt_choices, blank_choice='* Alla distrikt', blank_choice_value=0, required=False)


class NewBookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = (
            'when', 'street', 'zipcode', 'city',
            'club', 'notes', 'price',
            'max_participants', 'lat', 'lon',
        )
        widgets = {
            'notes': Textarea(attrs={'cols': 80, 'rows': 20}),
        }

    dicipline = DefaultChoiceField(choices=dicipline_choices, blank_choice='* Välj dicipline', blank_choice_value='0')
    duration = DefaultChoiceField(choices=duration_choices, blank_choice='* Träningens längd', blank_choice_value='0')
    county = DefaultChoiceField(choices=distrikt_choices, blank_choice='* Välj distrikt', blank_choice_value='0')
