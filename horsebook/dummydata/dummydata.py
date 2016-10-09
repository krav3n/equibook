# -*- coding: utf-8 -*-

import random
from datetime import datetime

# django imports
from django.contrib.auth.models import User

# horsebook imports
from horsebook.booking.models import Booking, BookingRow
from horsebook.trainer.models import Trainer, TrainerDicipline
from horsebook.student.models import Student

# 3rd party
from localflavor.se.forms import COUNTY_CHOICES


def random_string(l=8):
    return ''.join(random.choice('A' + 'B' + 'C' + 'D' + 'E' + 'F' + 'G' + 'H') for i in range(l))


def random_int(l=5):
    return ''.join(random.choice('1' + '2' + '3' + '4' + '5' + '6' + '7' + '8' + '9' + '0') for i in range(l))


def bio_gen(l=500):
    return ''.join(random.choice("a" + "b" + "c" + "d" + " ") for i in range(l))


def random_date():
    """
    Creates a random date
    """
    year = random.choice(range(2015, 2016))
    month = random.choice(range(1, 13))
    day = random.choice(range(1, 29))
    return datetime(year, month, day)


def create_trainer_dicipline_levels():
    """
    Helper method to create all trainer dicipline levels.
    """
    matrix = [
        ('A', 'Dressyr'),
        ('B', 'Hoppning'),
        ('C', 'Fälttävlan'),
        ('D', 'Tömkörning'),
        ('E', 'Löshoppning'),
        ('F', 'Sadelutprovare'),
        ('G', 'Akademisk Ridning'),
        ('H', 'Western'),
        ('I', 'Working Equitation'),
    ]

    for name in matrix:
        t = TrainerDicipline(code=name[0], name=name[1])
        t.save()


def mkusers(num=20):
    """
    Create predefined set of users to the test system
    """
    print("Creating users")

    user_map = {}
    all_trainer_diciplines = TrainerDicipline.objects.all()

    def make(username, email, password, is_active, is_staff, is_superuser):
        u = User.objects.create_user(username, email, password)
        u.first_name = username
        u.last_name = "{}sson".format(username)
        u.is_active = is_active
        u.is_staff = is_staff
        u.is_superuser = is_superuser
        u.save()

        # user_map[username] = u

        return u

    def make_trainer(username, user_obj):
        t = Trainer()
        t.name = user_obj.username
        t.phone = random_int()
        t.email = user_obj.email
        t.user = user_obj
        t.homepage = random_string()
        t.skill_level = random.choice(Trainer.LEVEL_CHOICES)[0]
        t.bio = bio_gen()
        t.county = random.choice(COUNTY_CHOICES)[0]
        t.save()

        for i in range(0, random.randint(1, 3)):
            r = random.choice(all_trainer_diciplines)
            r.trainer_set.add(t)
            r.save()

    def make_student(username, user_obj):
        s = Student()
        s.name = user_obj.username
        s.phone = random_int()
        s.email = user_obj.email
        s.user = user_obj
        s.save()

    # Make default users
    make('dev', 'dev@dev.se', 'barfoo', True, True, True)
    make('devuser', 'devuser@devuser.se', 'barfoo', True, True, False)
    tr = make('trainer', 'devuser@devuser.se', 'barfoo', True, True, False)
    st = make('student', 'devuser@devuser.se', 'barfoo', True, True, False)
    make_trainer(tr.username, tr)
    make_student(st.username, st)

    for i in range(num):
        username = random_string()
        email = "{}@{}.se".format(username, username)
        u = make(username, email, 'barfoo', True, True, False)
        user_map[username] = u

    for username, user_obj in user_map.items():
        if random.choice([True, False]):
            make_trainer(username, user_obj)
        else:
            make_student(username, user_obj)


def mkbookings(num=20, num_bookings=20):
    """
    Create predefined set of bookings
    """
    print("Creating Bookings & BookingRows")

    club_prefixes = ['Upp', 'Mitt', 'Syd', 'Norr', 'Center', 'Left', 'Right']

    all_trainers = Trainer.objects.all()
    all_students = Student.objects.all()

    for i in range(0, num):
        bo = Booking()
        bo.trainer = random.choice(all_trainers)
        bo.when = random_date()
        bo.street = random_string(l=8) + " Vägen"
        bo.zipcode = random_int(l=5)
        bo.city = random.choice(COUNTY_CHOICES)[0]
        bo.county = random.choice(COUNTY_CHOICES)[0]
        bo.club = random.choice(club_prefixes)[0] + " rid"
        bo.max_participants = random.randint(1, 4)
        bo.price = random.randint(300, 1200)
        bo.notes = bio_gen()
        bo.state = random.choice(Booking.STATES)
        bo.happened = random.choice([True, False])
        bo.lat = random.uniform(-70, 70)
        bo.lon = random.uniform(-180, 180)
        bo.trainer_set_coordinates = random.choice([True, False])
        bo.canceled_notes = bio_gen()
        bo.dicipline = random.choice(Booking.DICIPLINE_CHOICES)[0]
        bo.save()

    all_bookings = Booking.objects.all()

    for i in range(0, num_bookings):
        br = BookingRow()
        br.payment = BookingRow.PAYMENT_STRIPE
        br.status = random.choice(BookingRow.STATES)

        b = None
        while True:
            b = random.choice(all_bookings)
            if not b.booking_full():
                break

        br.booking = b
        br.student = random.choice(all_students)
        br.abort_reason = "I wanted to..."
        br.save()
