#http imports
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

#User imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import models
from models import LeadUserInfo

#forms
from forms.user_registration_form import UserForm, InfoForm
import forms.reset_password_form

import copy

import inventories

#We don't want logged in user to access certain pages (like the login page, so they can log in again)
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
    for inventory_id, cls in inventories.inventoryById.items():
        submissions = models.Submission.objects.filter(
            user=request.user, inventory_id=inventory_id
        )
        
        entry = {'inventory_id': inventory_id, 
            'name': cls.name}
        entry['taken'] = len(submissions) != 0
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
        return render(request, 'login.html')

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
        
    return render(request, 'reset_password_page.html', 
        {'form': form, 'success': success})

@login_required(redirect_field_name = None)      
#Logs out a user and redirects to the home page
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")
     
def validate_inventory_id(inventory_id):
    try:
        inventory_id = int(inventory_id)
    except ValueError:
        return False
    
    return inventory_id in inventories.inventoryById 

@login_required(redirect_field_name = None)  
def take_inventory(request, inventory_id):
    success = False
     
    if validate_inventory_id(inventory_id):    
        inventory = inventories.inventoryById[int(inventory_id)]()
    else:
        return page_not_found(request)
    
    submissions = models.Submission.objects.filter(
        user=request.user, inventory_id=inventory_id
    )
    already_taken = len(submissions) != 0
    
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
    
    show_form = not (success or already_taken)
    data = {'inventory': inventory, 'form': form,
        'success': success, 'already_taken': already_taken,
        'show_form': show_form}
    template = 'take_inventory/{}'.format(inventory.template)
  
    return render(request, template, data)
    
@login_required(redirect_field_name = None)
def review_inventory(request, inventory_id):
    if validate_inventory_id(inventory_id):    
        inventory = inventories.inventoryById[int(inventory_id)]()
    else:
        return page_not_found(request)
        
    submissions = models.Submission.objects.filter(
        user=request.user, inventory_id=inventory_id
    )
    metrics = models.Metric.objects.filter(submission=submissions)
    
    data = {'inventory': inventory, 'metrics': metrics}
    template = 'review_inventory/{}'.format(inventory.template)
    
    return render(request, template, data)

#If the user types in an incorrect url or somehow follows a bad link
@login_required(redirect_field_name = None)
def page_not_found(request):
    return render(request, 'page_not_found.html')
