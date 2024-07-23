
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .utils import errorAndReturn

def user(request):
    """
    Django view who display the user profile
    """
    if request.user.is_authenticated:
        return render(request, "login/user.html", {
        "title": f"{request.user.username}'s - Profile"
    })
    return HttpResponseRedirect(reverse("login"))

def logout_view(request):
    """
    Django view who logout the user then redirect it to the login page
    """
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return HttpResponseRedirect(reverse("login"))

def login_view(request):
    """
    Django view who render the login page or try to login the user if it's a POST
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user"))

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.warning(request, 'Invalid login or password.')
            return render(request, "login/loginForm.html", {
        "title": "Login"
    })

    return render(request, "login/loginForm.html", {
        "title": "Login"
    })

def register_view(request):
    """
    Django view who render the register page and haddle the register POST who create the user
    """
    if request.method == "POST":
        username = request.POST.get('username')
        
        if username != request.POST.get('username').strip(): # Make sure there is no whitespaces in the username
            return errorAndReturn(request, 'Username can\'t contain whitespaces.', "login/registerForm.html")
        
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2: # Make sure the passwords match
            return errorAndReturn(request, 'Passwords do not match.', "login/registerForm.html")
        try:
            user = User.objects.create_user(username, None,  password1)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("user"))
        except IntegrityError:
            return errorAndReturn(request, 'Username already taken.', "login/registerForm.html")
        except ValueError as ve:
            return errorAndReturn(request, str(ve), "login/registerForm.html")
    return render(request, "login/registerForm.html", {
        'title': 'Register'
    })