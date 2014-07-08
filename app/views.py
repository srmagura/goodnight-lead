#http imports
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse

#User imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

#Model imports
import models
from models import LeadUserInfo

#forms
from forms.user_registration_form import UserForm, InfoForm, UserSettingsForm, PasswordChangeForm
import forms.reset_password_form
from django.forms.models import model_to_dict

#Inventory inports
import inventories
from inventories.views import get_submission, submission_is_complete

#Other imports
import copy
from django.contrib import messages

#We don't want logged in users to access certain pages (like the login page, so they can log in again)
#If they're already logged in, redirect to the home page
def logout_required(function):
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            if request.user.is_authenticated():
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


@login_required(redirect_field_name = None)
def index(request):
    entries = []
    for inventory_id, cls in inventories.inventory_by_id.items():
        submission = get_submission(request.user, inventory_id)
        is_complete = submission_is_complete(submission)

        entry = {'inventory_id': inventory_id,
            'name': cls.name,
            'is_complete': is_complete,
            'is_started': submission is not None}
        entries.append(entry)

    data = {'inventories': entries}
    return render(request, 'index.html', data)

#Loads the login page.
@logout_required
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # Return a 'disabled account' error message
                return HttpResponse('disabled')
        else:
            return HttpResponse('Incorrect username or password')
    else:
        return render(request, 'user_templates/login.html')

#Loads the page for registering a new user with proper form validation
@logout_required
def register(request):
    #Process the form if it has been submitted through post
    if request.method == 'POST':

        #Get the form corresponding to the post data
        userForm = UserForm(request.POST)
        infoForm = InfoForm(request.POST)
        forms = [userForm, infoForm]

        #All validation rules pass - generate a new user account
        if all(form.is_valid() for form in forms):
            user = userForm.save()

            info = infoForm.save(commit=False)
            info.user = user
            info.save()

            #log the user in
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)

            #Redirect back to the login page, sending a success message
            messages.success(request, 'User account created successfully.')
            return HttpResponseRedirect(reverse('index'))

    #Get a blank form if loaded from link (initial load)
    else:
        userForm = UserForm()
        infoForm = InfoForm()

    #Render the page using whichever form was loaded.
    return render(
        request,
        'user_templates/register.html',
        {
            'userForm': userForm,
            'infoForm': infoForm,
        }
    )

@logout_required
def reset_password_page(request):
    form_cls = forms.reset_password_form.SendEmailForm
    success = False

    if request.method == 'POST':
        form = form_cls(request.POST)
        if form.is_valid():
            success = True
            form = form_cls()
    else:
        form = form_cls()

    return render(request,
        'user_templates/reset_password_page.html',
        {'form': form, 'success': success}
    )

@login_required(redirect_field_name = None)
#Logs out a user and redirects to the home page
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

#If the user types in an incorrect url or somehow follows a bad link
@login_required(redirect_field_name = None)
def page_not_found(request):
    return render(request, 'page_not_found.html')
