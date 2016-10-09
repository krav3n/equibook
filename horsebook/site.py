# -*- coding: utf-8 -*-

# python std lib
from functools import wraps

# django
from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm


class HorsebookAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form for backend admin site login.
    """
    this_is_the_login_form = forms.BooleanField(
        widget=forms.HiddenInput,
        initial=1,
        error_messages={'required': "Please log in again, because your session has expired."},
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = "Please enter the correct username and password"

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(message)
            elif not self.user_cache.is_active:
                raise forms.ValidationError(message)

        return self.cleaned_data


class BaseSite(admin.AdminSite):
    """
    """
    # login_template = 'login.html'
    logout_template = 'logout.html'
    login_form = HorsebookAuthenticationForm

    def __init__(self, name=settings.BASE_SITE_NAME):
        super(BaseSite, self).__init__(name)

site = BaseSite()

# Monkey patch this feature out because this action is enabled by default
site.disable_action('delete_selected')


def login_required(view_func):
    """
    Decorator for views that checks that the user is logged in.

    Displaying the login page if necessary.
    """
    @wraps(view_func)
    def _checklogin(request, *args, **kwargs):
        if request.user.is_active:
            # The user is valid. Continue to the admin page.
            return view_func(request, *args, **kwargs)
        return site.login(request)
    return _checklogin
