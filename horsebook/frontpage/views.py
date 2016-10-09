# coding=utf-8

from datetime import datetime

# horsebook imports
from horsebook.booking.models import Booking, BookingRow
from horsebook.search.api import search_all_bookings, search_all_trainers, last_minute_search
from horsebook.search.utils import ObjectPaginator
from horsebook.student.models import Student
from horsebook.trainer.models import Trainer
from horsebook.frontpage.forms import FirstPageForm, BookingSearchForm, ProfileSearchForm, NewBookingForm
from horsebook.frontpage.cache import memcache_set

# django imports
from django.core.paginator import EmptyPage
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render


def show(request):
    form = FirstPageForm()

    @memcache_set(60)
    def num_bookings():
        return Booking.objects.count()

    @memcache_set(60)
    def num_booking_rows():
        return BookingRow.objects.count()

    @memcache_set(60)
    def num_trainers():
        return Trainer.objects.count()

    @memcache_set(60)
    def num_students():
        return Student.objects.count()

    trainings = last_minute_search(9)

    return render(request, 'frontpage.html', {
        'form': form,
        'num_bookings': num_bookings(),
        'num_booking_rows': num_booking_rows(),
        'num_trainers': num_trainers(),
        'num_students': num_students(),
        'last_minute_trainings': trainings,
    })


def profile(request, id=None):
    if id is None:
        # No profile was selected so render my own profile
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/')
        id = request.user.id

    t = User.objects.filter(id=id).first()

    if not t:
        raise Http404

    bookings = None

    # If user is trainer then list the 10 upcomming bookings
    if hasattr(t, 'trainer'):
        # All trainers should be possible to view by everyone
        bookings = Booking.objects.filter(trainer=t.trainer).order_by('when')[:5]

        # Extract and optimize this here instead of in tempalte where it is difficult to make
        diciplines = ", ".join(t.trainer.diciplines.all().values_list("name", flat=True))
    elif hasattr(t, 'student'):
        # Only you should be able to view your profile
        if t != request.user:
            raise Http404

        bookings = Booking.objects.filter(bookingrow__student=t.student).order_by('when')[:5]

        diciplines = ""
    else:
        # just in case...
        raise Http404

    return render(request, 'profile.html', {
        'profile': t,
        'bookings': bookings,
        'diciplines': diciplines,
    })


def schema(request, id=None):
    """
    View either a trainers schema or your own.
    """
    if id is None:
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/')
        id = request.user.id

    t = User.objects.filter(id=id).first()

    if not t:
        raise Http404

    if hasattr(t, 'trainer'):
        bookings = Booking.objects.filter(trainer=t.trainer).order_by('-when')[:10]

        z = []
        for booking in bookings:
            z.append((booking, []))
    elif hasattr(t, 'student'):
        # Only allow viewing of your own profile if you are logged in as a student
        if t != request.user:
            raise Http404

        payments = BookingRow.objects.filter(student=t.student).order_by('created')[:10]
        bookings = [row.booking for row in payments]
        z = zip(bookings, payments)
    else:
        # just in case...
        raise Http404

    is_my_profile = False
    if hasattr(request.user, 'trainer') and t.trainer.id == request.user.trainer.id:
        is_my_profile = True

    return render(request, 'profile_schema.html', {
        'my_profile': is_my_profile,
        'profile': t,
        'z': z,
    })


def payments(request):
    t = request.user

    if hasattr(t, 'student'):
        payments = BookingRow.objects.filter(student=t.student).order_by('created')[:10]
    elif hasattr(t, 'trainer'):
        payments = BookingRow.objects.filter(booking__trainer=t.trainer).order_by('created')[:10]
    else:
        # Just in case O.o
        raise Http404

    return render(request, 'profile_payments.html', {
        'profile': t,
        'payments': payments,
    })


def settings(request):
    t = request.user
    return render(request, 'profile_settings.html', {'profile': t})


def faq(request):
    return render(request, 'faq.html', {})


def register(request):
    return render(request, 'register.html', {})


def logout(request):
    # TODO: Trigger logout code here...
    return HttpResponseRedirect('/')


def login(request):
    return render(request, 'login.html', {})


def do_login(request):
    next = request.POST['next'] if 'next' in request.POST else '/profile'
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            django_login(request, user)
            return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect('/login')
    else:
        return HttpResponseRedirect('/login')


def all_trainings(request):
    """
    """
    form = BookingSearchForm(request.GET, initial=request.GET)
    if not form.is_valid():
        print(form.errors)
        # TODO: Fix this case

    q = form.cleaned_data['q']
    county = form.cleaned_data['county']
    diciplines = form.cleaned_data['dicipline']
    show_full_boked = form.cleaned_data['show_full_boked']
    show_canceled = form.cleaned_data['show_canceled']
    show_done = form.cleaned_data['show_done']
    ordering = form.cleaned_data['ordering']
    max_price = form.cleaned_data['max_price']
    show_page = form.cleaned_data['page']

    if not show_page and 0 >= show_page:
        show_page = 1

    bookings = search_all_bookings(q, county, diciplines, max_price, show_full_boked, show_canceled, show_done, ordering)

    page = max(1, int(request.GET.get('page', show_page)))
    paginator = ObjectPaginator(bookings, 9, page, '', Booking, query_dict=request.GET.copy())

    try:
        p = paginator.current_page()
    except EmptyPage:
        p = None
    except Exception:
        paginator.current_index = paginator._num_pages
        p = paginator.page(paginator._num_pages)

    return render(request, 'booking_search.html', {
        'booking': bookings,
        'page': p,
        'paginator': paginator,
        'form': form
    })


def show_booking(request, id=None):
    if not id:
        raise Http404

    t = request.user

    if hasattr(t, 'student'):
        # Only a student can have a BookingRow instance
        my_booking_row = BookingRow.objects.filter(booking__id=id, student=t.student).first()
    else:
        my_booking_row = None

    booking = Booking.objects.get(pk=id)

    if not booking:
        raise Http404

    return render(request, 'booking_overview.html', {
        'booking': booking,
        'my_booking_row': my_booking_row,
    })


def kontakt(request):
    return render(request, 'kontakt.html', {})


def team(request):
    return render(request, 'team.html', {})


def newbooking(request):
    # TODO: Only allow trainer to use this endpoint

    form = NewBookingForm(initial=request.GET)

    return render(request, 'profile_new_booking.html', {
        'profile': request.user,
        'form': form,
    })


def make_new_booking(request):
    # TODO: Only allow trainer to use this endpoint
    form = NewBookingForm(request.GET)
    if form.is_valid():
        # TODO: Somehow validate that day is not in the past.
        b = Booking()
        b.trainer = request.user.trainer
        b.when = datetime.now()  # TODO:
        b.duration = form.cleaned_data['duration']
        b.dicipline = form.cleaned_data['dicipline']
        b.street = form.cleaned_data['street']
        b.zipcode = form.cleaned_data['zipcode']
        b.city = form.cleaned_data['city']
        b.county = form.cleaned_data['county']
        b.club = form.cleaned_data['club']
        b.notes = form.cleaned_data['notes']
        b.price = form.cleaned_data['price']
        b.max_participants = form.cleaned_data['max_participants']
        b.free_spots = form.cleaned_data['max_participants']
        b.lat = form.cleaned_data['lat']
        b.lon = form.cleaned_data['lon']
        b.trainer_set_coordinates = False  # TODO: Support this feature
        b.save()

        return render(request, 'profile_new_booking_ok.html', {
            'profile': request.user,
            'booking': b,
        })

    return render(request, 'profile_new_booking.html', {
        'profile': request.user,
        'form': form,
    })


def booking_map(request, id=None):
    if not id:
        raise Http404

    t = request.user

    booking = Booking.objects.get(pk=id)

    if hasattr(t, 'student'):
        # Only a student can have a BookingRow instance
        my_booking_row = BookingRow.objects.filter(booking__id=id, student=t.student).first()
    else:
        my_booking_row = None

    if not booking:
        raise Http404

    t = request.user
    return render(request, 'booking_map.html', {
        'profile': t,
        'booking': booking,
        'my_booking_row': my_booking_row,
    })


def booking_students(request, id=None):
    if not id:
        raise Http404

    booking = Booking.objects.get(pk=id)

    if not booking:
        raise Http404

    t = request.user
    return render(request, 'booking_students.html', {'profile': t, 'booking': booking})


def all_trainers(request):
    form = ProfileSearchForm(request.GET, initial=request.GET)
    if not form.is_valid():
        # TODO: Fix this case
        pass

    q = form.cleaned_data['q']
    county = form.cleaned_data['county']
    level = form.cleaned_data['level']
    diciplines = form.cleaned_data['dicipline']
    show_page = form.cleaned_data['page']

    if not show_page and 0 >= show_page:
        show_page = 1

    trainers = search_all_trainers(q, county, level, diciplines)

    page = int(request.GET.get('page', show_page))
    paginator = ObjectPaginator(trainers, 9, page, '', Trainer, query_dict=request.GET.copy())

    try:
        p = paginator.current_page()
    except EmptyPage:
        p = None
    except Exception:
        paginator.current_index = paginator._num_pages
        p = paginator.page(paginator._num_pages)

    return render(request, 'profile_search.html', {
        'trainers': trainers,
        'page': p,
        'paginator': paginator,
        'form': form
    })


def booking_reserv(request, id):
    """
    Render page for doing a booking
    """
    booking = Booking.objects.get(id=id)

    # TODO: Add hardcoded blocks for bookings that is full and should not be bookable.
    # TODO: If booking has not happened yet but it is full then queue system should be implemented

    return render(request, 'booking_reserv.html', {
        'booking': booking,
    })


def cancel_trainer(request, id):
    """
    Cancel a entire booking and issue a return payment for all students
    that have already paid or payment is processing.
    """
    t = request.user

    if hasattr(t, 'trainer'):
        booking = Booking.objects.get(id=id)

        if not booking:
            raise Http404

        if booking.trainer.id != t.trainer.id:
            # Booking is not your. Redirect to overview for booking.
            return HttpResponseRedirect('/booking/{}'.format(booking.id))

        return render(request, 'booking_cancel_trainer.html', {
            'booking': booking, 'profile': t,
        })
    else:
        # Only a trainer can use this endpoint
        return HttpResponseRedirect('/booking')


def cancel(request, id):
    """
    Cancel/Refund a paid booking. Usable by a student
    """
    t = request.user

    if hasattr(t, 'trainer'):
        # A trainer can't view this cancel view
        return HttpResponseRedirect('/booking')

    booking_row = BookingRow.objects.get(id=id)
    booking = booking_row.booking

    if not booking_row:
        # Booking row do not exist.
        return HttpResponseRedirect('/booking')

    if booking_row.student.id != t.student.id:
        # Booking is not your
        return HttpResponseRedirect('/booking')

    # TODO: Should only be possible to do by the person who made the booking row.
    return render(request, 'booking_cancel_student.html', {
        'booking_row': booking_row,
        'booking': booking,
    })


def payment_details(request, id):
    """
    View to show payment details
    """
    t = request.user
    payment = BookingRow.objects.get(id=id)

    if not payment:
        raise Http404

    # Validate that the user is allowed to view this payment
    if hasattr(t, 'trainer'):
        if payment.booking.trainer.id != t.trainer.id:
            return HttpResponseRedirect('/booking')
    elif hasattr(t, 'student'):
        if payment.student.id != t.student.id:
            return HttpResponseRedirect('/booking')
    else:
        # Just in case, should not happen
        raise Http404

    return render(request, 'profile_payment_details.html', {
        'profile': t,
        'payment': payment,
        'booking': payment.booking,
    })


def edit_booking(request, id):
    """
    """
    t = request.user
    booking = Booking.objects.get(id=id)

    if not booking:
        return HttpResponseRedirect('/booking')

    if hasattr(t, 'trainer'):
        if booking.trainer.id == t.trainer.id:
            form = NewBookingForm(instance=booking)
            return render(request, 'booking_edit.html', {
                'booking': booking,
                'profile': t,
                'form': form,
            })

    # Only a trainer shold be able to view
    return HttpResponseRedirect('/booking')
