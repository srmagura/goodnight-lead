#http imports
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect

#User imports
import django.contrib.auth as auth
from gl_site.custom_auth import login_required, logout_required

#forms
from gl_site.forms.user_registration_form import UserForm, InfoRegistrationForm
import gl_site.forms.reset_password_form as reset_password_form

#Inventory imports
from gl_site.inventories import inventory_by_id
from gl_site.inventories.views import get_submission, submission_is_complete

# Model imports
from gl_site.models import Session, LeadUserInfo
from gl_site.config_models import SiteConfig, DashboardText

#Other imports
import random
from django.contrib import messages
from gl_site.quotes.dashboard import quotes as dashboard_quotes

@login_required
def dashboard(request):
    """
    The dashboard view, i.e. the homepage that logged-in users see.
    """
    entries = []
    for inventory_id, cls in inventory_by_id.items():
        submission = get_submission(request.user, inventory_id)
        is_complete = submission_is_complete(submission)

        entry = {'inventory_id': inventory_id,
            'name': cls.name,
            'is_complete': is_complete,
            'is_started': submission is not None}
        entries.append(entry)

    shuffled_quotes = list(dashboard_quotes)
    random.shuffle(shuffled_quotes)

    dashbaord_text = DashboardText.objects.all()[0]

    data = {
        'inventories': entries,
        'quotes': shuffled_quotes,
        'inventory_desc': dashbaord_text.inventory_desc,
        'mental_health_warning': dashbaord_text.mental_health_warning,
        'about_panel_title': dashbaord_text.about_panel_title,
        'about_panel_contents': dashbaord_text.about_panel_contents,
    }
    return render(request, 'dashboard.html', data)

@logout_required
def login(request):
    """
    The login view, i.e. the first page that a new or unauthenticated user
    sees upon visiting our site.

    Logged-in users are not allowed to view this page.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        valid = True

        if user is None:
            valid = False
            message = 'Incorrect username or password.'
        elif not user.is_active:
            valid = False
            message = 'Account is disabled.'
        else:
            lead_user_info = LeadUserInfo.objects.filter(user=user)
            if not lead_user_info.exists():
                valid = False
                message = ('Your account has no associated demographic '
                    'information, and thus you are not allowed to login. '
                    'This can only occur if your account was not created '
                    'through the user registration form. '
                    'If you are an administrator, you can still login to '
                    'the admin site. If you would like to access the public '
                    'part of the site, please create a new account through '
                    'the user registration form.')

        if valid:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, message)

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
        info_form = InfoRegistrationForm(request.POST, session_uuid=session.uuid)
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
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
            auth.login(request, user)

            #Redirect back to the login page, sending a success message
            messages.success(request, 'User account created successfully.')
            return HttpResponseRedirect(reverse('dashboard'))

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
            'session_uuid': session_uuid,
            'action_url': request.build_absolute_uri(),
            'organization': session.organization,
            'session': session
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

def logout_user(request):
    """
    Logs out a user and redirects to the login page
    """
    auth.logout(request)
    return HttpResponseRedirect("/")

def page_not_found(request):
    """
    If the user types in an incorrect url or somehow follows a bad link
    """
    return render(request, 'page_not_found.html')

def set_base_url(request):
    """
    Use the request object to set SiteConfig.base_url.
    """
    base_url = request.build_absolute_uri('/')[:-1]
    config_query = SiteConfig.objects.all()

    if config_query.exists():
        config = config_query[0]
        config.base_url = base_url
    else:
        config = SiteConfig(base_url=base_url)

    config.save()

    return render(request, 'set_base_url.html',
        {'base_url': base_url})
