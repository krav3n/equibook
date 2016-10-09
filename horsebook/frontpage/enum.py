# coding=utf-8
"""
Enum backported from Python 3.4 with extra methods to make choices for model fields
See docs at https://pypi.python.org/pypi/enum34

>>> class PropertySort(Enum):
...     NAME = 1
...     SEARCH = 2
...     CUSTOM_SORT = 3
...
...     __verbose__ = {
...         NAME: (u"Namn", u"Some helptext"),
...         SEARCH: u"Sökträff",
...     }
...
>>> PropertySort.choices() == [(1, u'Namn'), (2, u'Sökträff'), (3, u'Custom sort')]
True
>>> PropertySort.default()
1
"""
from __future__ import absolute_import
import enum


class Enum(enum.Enum):
    __verbose__ = {}

    def verbose(self):
        v = self.__verbose__.get(self._value_)
        if isinstance(v, tuple):  # i.e. (verbose, helptext)
            return v[0]
        elif v:
            return v
        else:
            return unicode(self.name.replace('_', ' ').capitalize())

    @classmethod
    def choices(cls):
        return [(item.value, item.verbose()) for item in cls]

    @classmethod
    def default(cls):
        return getattr(cls, '__default__', list(cls)[0].value)
