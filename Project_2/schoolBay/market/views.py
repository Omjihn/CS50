from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect('/user/')
    return HttpResponse(f"Hello {request.user.username}")
