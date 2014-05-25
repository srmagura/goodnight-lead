from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from forms import UserRegistrationForm

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
		form = UserRegistrationForm(request.POST) 

		#All validation rules pass - generate a new user account
		if form.is_valid():			
			#Generate a new user and save, username, email, and password are required.
			user = User.objects.create_user(
				form.cleaned_data['username'],
				form.cleaned_data['email'],
				form.cleaned_data['password'],
				first_name = form.cleaned_data['firstname'],
				last_name = form.cleaned_data['lastname']
			)
			user.save()
			
			#Redirect back to the login page
			return HttpResponseRedirect('/')
			
	#Get a blank form if loaded from link (initial load)
	else:
		form = UserRegistrationForm()
        
    #Render the page using whichever form was loaded.
	return render(request, 'register.html', {
        'form': form,
    })