# coding=utf-8

import cPickle
import functools
import hashlib
import inspect
import types

from logging import error, warn

from django.conf import settings
from django.core.cache import get_cache


def cache(prefetch=None, require=[], process=None, ):
    """
    Decorator that caches calls to a method, i.e. only the first call will be
    executed.

    prefetch -- SQL that prefetches the data (optional). If this is specified
        the method will not be called at all since the value is prefetched.
    require -- Other cached fields required for the SQL (optional)
    process -- Function (arguments are self, value) that will be executed each
        time the value is returned (optional)
    """

    def wrap(fn):
        cache_name = '_extra_' + fn.__name__

        def wrapper(self, *args, **kwargs):
            if not hasattr(self, cache_name):
                warn('WAS NOT PREFETCHED: ' + fn.__name__)
                value = fn(self, *args, **kwargs)
                setattr(self, cache_name, value)
            elif settings.DEBUG and settings.DEBUG_CACHE:
                org = fn(self, *args, **kwargs)
                cached = getattr(self, cache_name)
                cached = process(self, cached) if process else cached
                if cached != org:
                    error('CACHED VALUE[' + str(cached) + '] for ' + fn.__name__ + ' DIFFER FROM CALCULATED[' + str(org) + ']!')
                    raise ValueError('CACHED VALUE[' + str(cached) + '] for ' + fn.__name__ + ' DIFFER FROM CALCULATED[' + str(org) + ']!')
            ret_value = getattr(self, cache_name)
            ret_value = process(self, ret_value) if process else ret_value
            return ret_value

        if prefetch and not isinstance(prefetch, types.FunctionType):
            wrapper._cache_prefetch = prefetch
            if require:
                wrapper._cache_require = require
            wrapper.admin_order_field = cache_name
        wrapper._cache_name = cache_name
        wrapper._cache_wrapped_name = fn.__name__
        return wrapper

    # If decorator is called without arguments the first argument is the
    # decorated function.
    if isinstance(prefetch, types.FunctionType):
        return wrap(prefetch)

    # Else we return a function that will be given the decorated function as its
    # first argument
    return wrap


def _is_cache_decorated(m):
    return inspect.ismethod(m) and hasattr(m, '_cache_prefetch')


def _caches(Model):
    attrs = []
    for attr in dir(Model):
        try:
            attrs.append(getattr(Model, attr))
        # In some cases, a Django field may show up as a class attribute and
        # should be ignored
        except AttributeError:
            pass
    return dict([
                (cache._cache_name, {'cache': cache, 'required': False})
                for cache in attrs if _is_cache_decorated(cache)])


def get_extra_select(Model, cached=[]):
    """
    Generate a dictionary with select extras to be used with QuerySet.extra method.

    Model -- The model for which the extras should be generated
    cached -- A list of cached values that are required (optional). If omitted
        all cached values will be fetched.
    """
    caches = _caches(Model)

    required_names = {}

    # Find extras that are required by other extras
    for name, cache in caches.items():
        if hasattr(cache['cache'], '_cache_require'):
            for require in cache['cache']._cache_require:
                caches[require._cache_name]['required'] = True
                required_names[require._cache_wrapped_name] = require._cache_name

    # Create extra select
    select = {}

    # If cached is empty we will cache everything
    requested_to_be_cached = [i for i in caches.items() if not cached or (i[1]['cache']._cache_wrapped_name in cached or i[1]['cache']._cache_wrapped_name in required_names)]

    for name, cache in requested_to_be_cached:
        if cache['required']:
            sql = '@' + name + ' := (' + cache['cache']._cache_prefetch % required_names + ')'
        else:
            sql = cache['cache']._cache_prefetch % required_names
        select[name] = sql

    return select


def get_cached(qs, Model, cached=[]):
    """
    Extend queryset to fetch extras associated with a Model.

    qs -- QuerySet to be extended
    Model -- The model for which the extras should be generated
    cached -- A list of cached values that are required (optional). If omitted
        all cached values will be fetched.
    """
    return qs.extra(select=get_extra_select(Model, cached=cached))


def memcache_set(time):
    """
    Used to decorate method using memcache. Function creates unique key in memcache storage and store there data which are cached.
    Function allows to cache every method, even if we have there an ORM.

    :param time: how long we should keep cached data, in seconds
                 there is no default for time because you must know what you are doing
    """

    MEMCACHE_DECORATOR_PREFIX = '__memcache_decorator__'

    def _get_cache_key(fn, *args, **kwargs):
        """
        Generates unique key for data which we want to cache.
        """
        module = fn.__module__ or ''
        name = MEMCACHE_DECORATOR_PREFIX + module + '_' + fn.__name__

        serialise = [name, ]

        for arg in args:
            serialise.append(arg)

        for key, arg in kwargs.items():
            serialise.append(key)
            serialise.append(arg)

        key = hashlib.md5(cPickle.dumps(serialise)).hexdigest()
        return key

    cache = get_cache(settings.CACHE_MIDDLEWARE_ALIAS)

    def __delete_cache(_key, warning):
        """
        The real function to delete cache
        """
        def func():
            if not warning:
                cache.delete(_key)
            else:
                raise Exception('delete_cache() is not valid for this method/function')

        return func

    def __call_delete_cache(_wrapper):
        """
        Outside `_wrapper`, `key` is unknown.
        This function calls inner `_delete_cache` in `_wrapper`
        """
        def func():
            if hasattr(_wrapper, '_delete_cache'):
                _wrapper._delete_cache()

        return func

    def decorator(fn):
        """
        Gets data from cache. If data does not exist we store it within cache.
        Decorator creates different key for different variation of method  i.e. test(1,2), test(4,5) have different key.

        `delete_cache()` can be called for every function which uses this decorator.
        """
        from inspect import getargspec
        import types

        warning = False

        spec = getargspec(fn)

        if types.FunctionType == type(fn):
            if spec.varargs is None and spec.keywords is None and spec.defaults is None and len(spec.args) == 0:
                pass
            else:
                warning = True

        elif types.MethodType == type(fn):
            if spec.varargs is None and spec.keywords is None and spec.defaults is None and len(spec.args) == 1 and spec.args[0] == 'self':
                pass
            else:
                warning = True

        else:
            warning = True

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):

            # unique key for cached object
            key = _get_cache_key(fn, *args, **kwargs)

            res = cache.get(key, None)

            if res is None:
                # if no hit to cache, save it in cache
                res = fn(*args, **kwargs)
                cache.set(key, res, time)

            setattr(wrapper, '_delete_cache', __delete_cache(key, warning))
            return res

        setattr(wrapper, 'delete_cache', __call_delete_cache(wrapper))
        return wrapper

    return decorator
