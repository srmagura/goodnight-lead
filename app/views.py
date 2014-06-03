#http imports
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

#User imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from models import LeadUserInfo

#forms
from forms.user_registration_form import UserForm, InfoForm
import forms.reset_password_form

import inventories

#Loads the login page.
def login_page(request):
    return render(request, 'login.html')

#Log a user in and display the correct response.
def do_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse('Logged in as {}'.format(username))
        else:                                  
            # Return a 'disabled account' error message
            pass
    else:
        return HttpResponse('Incorrect username or password')

#Loads the page for registering a new user with proper form validation
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
            user.set_password(user.password)
            user.save()
            
            info = infoForm.save(commit=False)
            info.user = user
            info.save()
            
            #Redirect back to the login page
            return HttpResponseRedirect('/')
            
    #Get a blank form if loaded from link (initial load)
    else:
        forms = [UserForm(), InfoForm()]
        
    #Render the page using whichever form was loaded.
    return render(request, 'register.html', {
        'forms': forms,
    })

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
        
    return render(request, 'reset_password_page.html', 
        {'form': form, 'success': success})
        
#Logs out a user and redirects to the home page
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")
     
@login_required   
def take_inventory(request, inventory_id):
    success = False
    inventory = inventories.inventoryById[int(inventory_id)]()
    form_cls = inventories.InventoryForm
    form_kwargs = {'inventory': inventory}
    
    if request.method == 'POST':
        form = form_cls(request.POST, **form_kwargs) 
        if form.is_valid():
            success = True
            inventory.submit(request.user, form)
            
            form = None
    else:       
        form = form_cls(**form_kwargs)
    
    data = {'inventory': inventory, 'form': form,
        'success': success}
    template = 'take_inventory/{}'.format(inventory.template)
  
    return render(request, template, data)

