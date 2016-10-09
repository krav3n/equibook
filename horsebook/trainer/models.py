# coding=utf-8

from django.db import models
from django.contrib.auth.models import User

from horsebook.common.db.models import TimestampedModel
from horsebook.frontpage.cache import memcache_set

from localflavor.se.forms import COUNTY_CHOICES


class TrainerDicipline(models.Model):
    """
    Each trainer can have multiple diciplines bound to their profile.
    """
    name = models.CharField(max_length=255, db_index=True, unique=True)
    code = models.CharField(max_length=255, db_index=True, unique=True)

    def __unicode__(self):
        return u'{0}'.format(self.name)


class Trainer(TimestampedModel):
    LEVEL_A_TRAINER = 1
    LEVEL_B_TRAINER = 2
    LEVEL_C_TRAINER = 3
    LEVEL_ASPIRANT_A = 4
    LEVEL_ASPIRANT_B = 5
    LEVEL_ASPIRANT_C = 6
    LEVEL_DRESYR = 7
    LEVEL_INVERKANSDOMARE = 8
    LEVEL_A_ONLY = 9
    LEVEL_B_ONLY = 10
    LEVEL_MASTER = 11

    A_TRAINER = u"A-tränare"
    B_TRAINER = u"B-tränare"
    C_TRAINER = u"C-tränare"
    ASPIRANT_A = u"Aspirant A"
    ASPIRANT_B = u"Aspirant B"
    ASPIRANT_C = u"Aspirant C"
    DRESYR = u"Dressyr"
    INVERKANSDOMARE = u"Inverkansdomare"
    A_ONLY = u"A - enbart"
    B_ONLY = u"B - enbart"
    MASTER = u"Master"

    LEVEL_CHOICES = (
        (LEVEL_A_TRAINER, A_TRAINER),
        (LEVEL_B_TRAINER, B_TRAINER),
        (LEVEL_C_TRAINER, C_TRAINER),
        (LEVEL_ASPIRANT_A, ASPIRANT_A),
        (LEVEL_ASPIRANT_B, ASPIRANT_B),
        (LEVEL_ASPIRANT_C, ASPIRANT_C),
        (LEVEL_DRESYR, DRESYR),
        (LEVEL_INVERKANSDOMARE, INVERKANSDOMARE),
        (LEVEL_A_ONLY, A_ONLY),
        (LEVEL_B_ONLY, B_ONLY),
        (LEVEL_MASTER, MASTER),
    )
    LEVELS = [l[0] for l in LEVEL_CHOICES]
    LEVELS_MAP = {l[0]: l[1] for l in LEVEL_CHOICES}

    # Bind to internal django user
    user = models.OneToOneField(User, related_name='trainer', editable=False)

    # Skill level of this trainer
    skill_level = models.PositiveIntegerField(verbose_name='skill level', max_length=255, choices=LEVEL_CHOICES)

    # TODO: Ändra om name till first & last name
    name = models.CharField(verbose_name='trainer name', max_length=255, db_index=True)
    phone = models.CharField(verbose_name='trainer phone support', max_length=32)
    email = models.CharField(verbose_name='trainer email', max_length=32)

    # The skill diciplines that the trainer supports
    diciplines = models.ManyToManyField(TrainerDicipline)

    # Personal homepage link is a custom link to the trainer homepage
    homepage = models.URLField(verbose_name='trainer homepage', max_length=255)

    # A short summary of the user
    bio = models.CharField(verbose_name='biography', max_length=500)

    # These fields should be lazy updated because otherwise the database might
    # be overloaded with requests to constantly parse this value

    # This field should track the ammount of cash that has been confirmed that
    # belongs to them. It should handle that some of the money is lost in transaction
    # fees and that some belongs to us.
    total_earned = models.PositiveIntegerField(default=0)
    total_earned_month = models.PositiveIntegerField(default=0)
    total_earned_year = models.PositiveIntegerField(default=0)
    # TODO: Idea is to move these fields into something easier to work with
    #       like redis where it can handle the data because it is kinda volotile
    #       and can be reconstructed from all bookings and booking rows.

    # What district this trainer belongs to
    county = models.CharField(max_length=4, choices=COUNTY_CHOICES)

    class Meta:
        verbose_name = 'trainer'
        verbose_name_plural = 'trainers'
        permissions = ()

    def __unicode__(self):
        return self.name

    @memcache_set(60)
    def format_diciplines_string(self):
        """
        Helper method to render this string.
        Should be cached for some time to avoid expensive database lookups.
        """
        return ", ".join(self.diciplines.all().values_list("name", flat=True))
