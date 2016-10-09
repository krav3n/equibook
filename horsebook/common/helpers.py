# -*- coding: utf-8 -*-

# django imports
from django.conf import settings
from django.contrib.admin import helpers as admin_helpers
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.query_utils import Q
from django.shortcuts import render
from django.utils.encoding import force_unicode


def create_proxy(name, base, filter_args={}, exclude_args={}, meta={}, module=None):
    """
    Function creates proxy model for admin pages. Proxy models are 'virtual' tables but inherit real tables.

    filter_args and exclude_args can be lists, dictionaries or Q-objects.
    """
    if not module:
        module = base.__module__

    # Use custom manager or fallback to the default one
    base_manager_class = getattr(base, 'objects', None)
    if base_manager_class:

        if isinstance(base_manager_class, models.Manager):
            base_manager_class = base_manager_class.__class__

        # just in case, you never know...
        elif not issubclass(base_manager_class, models.Manager):
            base_manager_class = None

    if not base_manager_class:
        base_manager_class = models.Manager

    # Override manager.get_queryset()
    def get_queryset(self):
        qs = base_manager_class.get_queryset(self)
        if filter_args:
            if isinstance(filter_args, Q):
                qs = qs.filter(filter_args)
            else:
                qs = qs.filter(**filter_args)
        if exclude_args:
            if isinstance(exclude_args, list):
                for exclude_arg in exclude_args:
                    qs = qs.exclude(**exclude_arg)
            elif isinstance(exclude_args, Q):
                qs = qs.exclude(exclude_args)
            else:
                qs = qs.exclude(**exclude_args)
        return qs

    Manager = type(name + 'Manager', (base_manager_class,), {'get_queryset': get_queryset, '__module__': module})

    proxy_meta = {}

    # Inherit verbose_name and verbose_name_plural from base
    if hasattr(base, '_meta'):
        if hasattr(base._meta, 'verbose_name'):
            proxy_meta['verbose_name'] = base._meta.verbose_name
        if hasattr(base._meta, 'verbose_name_plural'):
            proxy_meta['verbose_name_plural'] = base._meta.verbose_name_plural

    proxy_meta.update(meta)

    proxy_meta['proxy'] = True

    return type(name, (base,), {'objects': Manager(), 'Meta': type('Meta', (object,), proxy_meta), '__module__': module})


class NotConfirmed(Exception):
    def __init__(self, response):
        self.response = response


def confirm(modeladmin, request, message, queryset, object_tree=None,
            form=None, template='admin/confirm.html',
            context_extra={}, admin_name=None):
    """
    The flow behind this function is the following. A request is sent to the model
    admin. This function is called. It will then check that request for a
    'confirmed' field in the request. If this field is not present it will throw
    an exception. This exception contains a HttpResponse which renders a confirm
    page showing the objects in object_tree.

    :param modeladmin:
        The modeladmin instance on which the action is executed.
    :type modeladmin:
        ModelAdmin
    :param request:
        The request containing the POST data
    :type request:
        HttpRequest
    :param message:
        A message to be shown on the top of the page e.g.
        "Are you sure you want to delete the following..."
    :type message:
        unicode
    :param queryset:
        The queryset containing all objects acted on
    :type queryset:
        QuerySet
    :param object_tree:
        The objects that should be shown to be confirmed. If
        omitted a flat tree is created from queryset
    :type object_tree:
        [(unicode, [(unicode, ...),...] or None (ends recursion), ...]
    :param form:
        A form which fields will be rendered as hidden to preserve data.
        This is used by the handle_action_form function.
    :type form:
        Form
    :param template:
        Alternative template for the confirm page
    :type template:
        unicode
    :param context_extra:
        Extra data to be updated to the context. I.e. this will
        override anything in the context created by this function
    :type context_extra:
        dict
    :param admin_name:
        name of admin site to use for urls resolving
    :type admin_name:
        str
    """
    opts = modeladmin.model._meta
    app_label = opts.app_label

    if 'confirmed' in request.POST:
        return None

    if not object_tree:
        object_tree = [(force_unicode(obj), None) for obj in queryset]

    form_action = get_objects_list_url(modeladmin.model, admin_name)
    context = {
        'title': "Confirm action",
        'message': message,
        'object_name': force_unicode(opts.verbose_name),
        'opts': opts,
        'app_label': app_label,
        'action_checkbox_name': admin_helpers.ACTION_CHECKBOX_NAME,
        'object_tree': object_tree,
        'queryset': queryset,
        'action': request.POST['action'],
        'form_action': form_action,
        'form': form,
    }
    context.update(context_extra)

    raise NotConfirmed(render(request, template, context))


def get_objects_list_url(model_class, admin_name=None):
    """
    Returns url to a list of Model objects under admin_name admin site.
    :param model_class: Model class to point to (for example, MerchantClaim, User, etc)
    :param admin_name: Admin site name (Staff admin site name by default)
    """
    admin_name = admin_name or settings.STAFF_ADMIN_SITE_NAME
    return reverse('{0}:{1}_{2}_changelist'.format(
        admin_name,
        model_class._meta.app_label,
        model_class._meta.model_name,
    ))
