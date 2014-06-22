#View imports
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

#Form imports
from app.forms.user_registration_form import UserForm, InfoForm, UserSettingsForm, PasswordChangeForm

#Messages
from django.contrib import messages

#Account information/settings view
@login_required(redirect_field_name = None)        
def account_settings(request):
    if(request.method == 'POST'):
        usersettingsform = UserSettingsForm(request.POST, instance=request.user)
        infoform = InfoForm(request.POST, instance=request.user.leaduserinfo)
        forms = [usersettingsform, infoform]
        
        if all(form.is_valid() for form in forms):
            #Save the updated info
            usersettingsform.save()
            infoform.save()
            
            messages.success(request, 'Account Settings updated successfully')
            return HttpResponseRedirect('/')
            
    else:
        usersettingsform = UserSettingsForm(instance=request.user)
        infoform = InfoForm(instance=request.user.leaduserinfo)
        
    return render(
        request,
        'user_templates/account_settings.html',
        {
            'usersettingsform': usersettingsform,
            'infoform': infoform,
        }
    )
    
#Password change view
@login_required(redirect_field_name = None)
def password(request):
    if(request.method == 'POST'):
        passwordform = PasswordChangeForm(request.POST)

        if(passwordform.is_valid()):
            password = request.POST['password1']
            user = request.user
            user.set_password(password)
            user.save()
            
            messages.success(request, "Password set successfully")
            return HttpResponseRedirect(reverse('account-settings'))
        
    else:
        passwordform = PasswordChangeForm()
        
    return render(
        request,
        'user_templates/password.html',
        {'form': passwordform }
    )