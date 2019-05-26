"""Account views."""


# Imports
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from gl_site.custom_auth import login_required
from gl_site.forms.user_registration_form import InfoForm, UserSettingsForm, PasswordChangeForm


@login_required
def account_settings(request):
    """
    Account information/settings view
    """
    if(request.method == 'POST'):
        user_settings_form = UserSettingsForm(request.POST, instance=request.user)
        info_form = InfoForm(request.POST, instance=request.user.leaduserinfo)
        forms = [user_settings_form, info_form]

        if all(form.is_valid() for form in forms):
            #Save the updated info
            user_settings_form.save()
            info_form.save()

            messages.success(request, 'Account Settings updated successfully')
            return HttpResponseRedirect('/')

    else:
        user_settings_form = UserSettingsForm(instance=request.user)
        info_form = InfoForm(instance=request.user.leaduserinfo)

    return render(
        request,
        'user/settings.html',
        {
            'user_form': user_settings_form,
            'info_form': info_form,
            'action_url': request.build_absolute_uri(),
            'organization': request.user.leaduserinfo.organization,
            'session': request.user.leaduserinfo.session,
        }
    )

#Password change view
@login_required
def password(request):
    if(request.method == 'POST'):
        passwordform = PasswordChangeForm(request.POST)

        if(passwordform.is_valid()):
            userPassword = request.POST['password1']
            user = request.user
            user.set_password(userPassword)
            user.save()
            update_session_auth_hash(request, user)

            messages.success(request, "Password set successfully")
            return HttpResponseRedirect(reverse('account-settings'))

    else:
        passwordform = PasswordChangeForm()

    return render(
        request,
        'user/password.html',
        {'form': passwordform }
    )
