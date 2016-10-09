# coding=utf-8

# python stdlib
from os.path import join

# django imports
from django.core.paginator import Paginator

from django.db.models.query import QuerySet
from django.core.paginator import Page
from haystack.query import SearchQuerySet
from horsebook.booking.models import Booking
from horsebook.trainer.models import Trainer


class ObjectPaginator(Paginator):
    def __init__(self, objects, per_page, current_index, url, model, query_dict=None, edge=1, adjecent=2):
        super(ObjectPaginator, self).__init__(objects, per_page)
        self.current_index = current_index
        self.url = url
        self.edge = edge
        self.query_dict = query_dict.copy() if query_dict is not None else None

        # The code below excludes the last adjecent page (<adjecent)
        # By adding one here we change it to (<=adjecent) which is more
        # intuitive
        self.adjecent = adjecent + 1
        self.model = model

    def page(self, number):
        page = super(ObjectPaginator, self).page(number)

        if isinstance(page.object_list, QuerySet):
            ids = [product['pk'] for product in page.object_list.values('pk')]

            # keep same order by clause as used
            #   in paginator to fetch full product objects
            ordering = page.object_list.query.order_by
        elif isinstance(self.object_list, SearchQuerySet):
            # When this step happens just after the index was cleared, then product may be None
            # import pdb; pdb.set_trace()
            # ids = [product.pk for product in page.object_list if product is not None]
            ids = page.object_list

            # ordering = self.object_list._db_query_order  # our custom parameter to remember db order
            ordering = None
        else:
            raise

        if not ids:
            return Page([], number, self)

        product_set = self.model.objects.filter(id__in=ids)

        # ordering must by different than relevancy (relevancy occurs only in the elasticsearch part)
        if ordering and any(item not in ['relevancy', '-relevancy'] for item in ordering):
            product_set = product_set.order_by(*ordering)
        else:
            # it's a way to avoid automatically sorting by id. We want to have order which we get from the elasticsearch.
            # Especially useful when we search by id i.e. 400 (for this word we can find a lot of product by title and one by id).
            # We want to have the product which is found by id on the first position, so we should keep the list returned by solr.
            product_set = self.model.objects.filter(id__in=ids).extra(
                select={'manual': 'FIELD(id, %s)' % ','.join(map(str, ids))},
                order_by=['manual'],
            )

        # TODO: This is micro optimization for search to reduce number of queries
        if self.model == Booking:
            product_set = product_set.prefetch_related('trainer', 'trainer__user')
        elif self.model == Trainer:
            product_set = product_set.prefetch_related('user', 'diciplines')

        return Page(product_set, number, self)

    def page_url(self, index):
        if 'page' not in self.query_dict or not index:
            # Allways default to page 1
            self.query_dict['page'] = 1
        else:
            # If it is present then set the index
            self.query_dict['page'] = index

        query_string = '?' + self.query_dict.urlencode() if self.query_dict else ''

        return join(self.url, query_string)

    def current_page(self):
        return self.page(self.current_index)

    def has_next(self):
        return self.current_page().has_next()

    def has_previous(self):
        return self.current_page().has_previous()

    def next(self):
        return self.page_url(self.current_index + 1)

    def previous(self):
        return self.page_url(self.current_index - 1)

    def has_other_pages(self):
        return self.current_page().has_other_pages()

    def center(self):
        return [(index, self.page_url(index)) for index in self.page_range[max(0, self.current_index - self.adjecent):min(self.num_pages, self.current_index + self.adjecent - 1)]]

    def has_left_elipse(self):
        return self.current_index - self.adjecent > self.edge

    def left_edge(self):
        return [(index, self.page_url(index)) for index in self.page_range[:max(0, min(self.edge, self.current_index - self.adjecent))]]

    def has_right_elipse(self):
        return self.current_index + self.adjecent < self.num_pages - 1

    def right_edge(self):
        return [(index, self.page_url(index)) for index in self.page_range[min(self.num_pages, max(self.num_pages - self.edge, self.current_index + self.adjecent - 1)):]]
