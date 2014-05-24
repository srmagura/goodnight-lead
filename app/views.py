from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

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

#Loads the page for registering a new user.
def register_user_page(request):
	return render(request, 'register.html')
	
#Register a new user account and log in.
#TODO error checking.
def register_user(request):
	firstname = request.POST['firstname']
	lastname = request.POST['lastname']
	username = request.POST['username']
	email = request.POST['email']
	password = request.POST['password']
	
	user = User.objects.create_user(username, email, password, first_name=firstname, last_name=lastname)
	user.save()
	
	return render(request, 'login.html');