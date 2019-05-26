"""
Function decorators for authentication that are specific to our app.

USE THE login_required FROM THIS MODULE INSTEAD OF DJANGO'S BUILT-IN
login_required.
"""
from django.http import HttpResponseRedirect
from django.conf import settings

import django.contrib.auth as auth

from gl_site.models import LeadUserInfo

def is_authorized(request):
    """
    Return whether or not the user has access to our app (gl_site).

    In addition to being authenticated normally, the user must have
    an associated LeadUserInfo. LeadUserInfo is not required to login
    to the admin site.
    """
    if not request.user.is_authenticated:
        return False

    lead_user_info = LeadUserInfo.objects.filter(user=request.user)
    if not lead_user_info.exists():
        auth.logout(request)
        return False

    return True

def login_required(function):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the login page if necessary.

    USE THIS DECORATOR INSTEAD OF DJANGO'S BUILT-IN login_required.

    Differences from the built-in login_required:
    - Check that the user also has an associated LeadUserInfo object
    - Set default direct_field_name to None
    """
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            if is_authorized(request):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(settings.LOGIN_URL)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)

def logout_required(function):
    """
    We don't want logged in users to access certain pages (like the login
    page.) If they're already logged in, redirect to the dashboard.
    """
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            if is_authorized(request):
                return HttpResponseRedirect('/')
            else:
                return view_func(request, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)
