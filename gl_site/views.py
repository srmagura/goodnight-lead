#http imports
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

#User imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#forms
from gl_site.forms.user_registration_form import UserForm, InfoRegistrationForm
import gl_site.forms.reset_password_form as reset_password_form

#Inventory imports
from gl_site.inventories import inventory_by_id
from gl_site.inventories.views import get_submission, submission_is_complete

# Model imports
from gl_site.models import Session

#Other imports
from django.contrib import messages
from gl_site.quotes.indexQuotes import quoteList as indexQuotes

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
    for inventory_id, cls in inventory_by_id.items():
        submission = get_submission(request.user, inventory_id)
        is_complete = submission_is_complete(submission)

        entry = {'inventory_id': inventory_id,
            'name': cls.name,
            'is_complete': is_complete,
            'is_started': submission is not None}
        entries.append(entry)

    data = {'inventories': entries, 'quotes': indexQuotes}
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
            messages.warning(request, "Incorrect username or password")

    return render(request, 'user/login.html')

@logout_required
def register(request, session_uuid):
    """
    Loads the page for registering a new user with proper form validation
    """
    # Redirect away from the registration page if the uuid
    # is incorrect
    try:
        session = Session.objects.get(uuid=session_uuid)
    except Session.DoesNotExist:
        return HttpResponseRedirect(reverse('login'))

    #Process the form if it has been submitted through post
    if request.method == 'POST':

        #Get the form corresponding to the post data
        user_form = UserForm(request.POST)
        info_form = InfoRegistrationForm(request.POST)
        user_forms = [user_form, info_form]

        #All validation rules pass - generate a new user account
        if all(form.is_valid() for form in user_forms):
            user = user_form.save()

            info = info_form.save(commit=False)
            info.user = user

            info.session = session
            info.organization = session.organization

            info.save()

            #log the user in
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)

            #Redirect back to the login page, sending a success message
            messages.success(request, 'User account created successfully.')
            return HttpResponseRedirect(reverse('index'))

    #Get a blank form if loaded from link (initial load)
    else:
        user_form = UserForm()
        info_form = InfoRegistrationForm()

    #Render the page using whichever form was loaded.
    return render(
        request,
        'user/register.html',
        {
            'user_form': user_form,
            'info_form': info_form,
            'session_uuid': session_uuid
        }
    )

@logout_required
def reset_password_page(request):
    form_cls = reset_password_form.SendEmailForm
    success = False

    if request.method == 'POST':
        form = form_cls(request.POST)
        if form.is_valid():
            success = True
            form = form_cls()
    else:
        form = form_cls()

    return render(request,
        'user/reset_password_page.html',
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
