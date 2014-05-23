from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def login_page(request):
    return render(request, 'login.html')

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
