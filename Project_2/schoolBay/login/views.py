
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

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
            return HttpResponseRedirect(reverse("user"))
        else:
            return render(request, "login/loginForm.html", {
        "message": "Invalid login or password",
        "title": "Login"
    })

    return render(request, "login/loginForm.html", {
        "title": "Login"
    })
