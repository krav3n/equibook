# coding=utf-8

# horsebook imports
from horsebook.booking.models import Booking
from horsebook.trainer.models import Trainer

# haystack imports
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet


def order_by_id(model, object_ids, ordering='-id'):
    return model.objects.filter(
        pk__in=object_ids,
    ).order_by(ordering)


def to_es_bool(boolean_value):
    """
    Due to a bug/problem in elasticsearch, each boolean value that is used
    in a filter must be converted to a '1' or '0' for the server to handle it properly.
    """
    return '1' if boolean_value else '0'


def search_all_bookings(q, county, dicipline, max_price, show_full_boked, show_canceled, show_done, ordering):
    """
    Move later to search.api
    """
    sqs = SearchQuerySet().models(Booking)

    # TODO: Find out what this field should be used for O.o
    # if q is not None and q != '':
    #     sqs = sqs.filter(name=AutoQuery(q))

    if max_price is not None and max_price not in ('', '0'):
        sqs = sqs.filter(price__lt=max_price)

    states = [Booking.STATE_PLANNING]

    if show_canceled:
        states.append(Booking.STATE_CANCELED)

    if show_done:
        states.append(Booking.STATE_DONE)

    sqs = sqs.filter(state__in=states)

    if show_full_boked:
        sqs = sqs.filter_or(full=to_es_bool(show_full_boked))
    else:
        sqs = sqs.filter(full=to_es_bool(show_full_boked))

    if county is not None and county not in ('', '0'):
        sqs = sqs.filter(county=county)

    if dicipline is not None and dicipline not in ('', '0'):
        sqs = sqs.filter(dicipline=dicipline)

    # Ordering for the sql query
    ordering_mapping = {
        '': '-id',  # Default ordering by id
        'A': '-id',  # Datum
        'B': '-free_spots',  # Free spots
        'C': '-id',  # Booked spots
        'D': '-price',  # Most Expensive
        'E': 'price',  # Cheapest Price
    }
    sqs = sqs.order_by(ordering_mapping[ordering])

    print(sqs.query)

    # Extract all objects based on ES search
    # return order_by_id(Booking, sqs.values_list('pk', flat=True), ordering=ordering_mapping[ordering])
    return sqs.values_list('pk', flat=True)


def search_all_trainers(q, county, skill, diciplines):
    """
    Move later to search.api
    """
    model = Trainer
    sqs = SearchQuerySet().models(model)

    if q is not None and q not in ('', '0'):
        sqs = sqs.filter_or(name=AutoQuery(q))
        sqs = sqs.filter_or(email=AutoQuery(q))

    if county is not None and county not in ('', '0'):
        sqs = sqs.filter_or(county=county)

    if skill is not None and skill not in ('', '0'):
        sqs = sqs.filter_or(skill_level=skill)

    if diciplines is not None and diciplines not in ('', '0'):
        sqs = sqs.filter_or(diciplines=diciplines)

    # Extract all objects based on ES search
    # return order_by_id(model=model, object_ids=sqs.values_list('pk', flat=True))

    return sqs.values_list('pk', flat=True)


def last_minute_search(limit):
    """
    """
    model = Booking
    sqs = SearchQuerySet().models(model)

    sqs = sqs.filter(state__in=[Booking.STATE_PLANNING]).order_by('-when')

    return model.objects.filter(pk__in=sqs.values_list('pk', flat=True)[:limit])[:limit].prefetch_related('trainer', 'trainer__user')
