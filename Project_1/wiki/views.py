import markdown2
import json
import os, re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from markdown2 import Markdown

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from .utils import list_entries, modif_file, get_entry

# Create your views here.

def index(request):
    entries = list_entries()
    return render(request, 'wiki/index.html', {
        'entries': entries
    })

def page(request, name):

    if request.method == 'POST':
        new_content = request.POST.get('new_content')
        modif_file(name, new_content)
        return redirect(f'/wiki/{name}/')
    elif request.method == 'GET':
        content = get_entry(name)
        if content is None:
            return render(request, "wiki/error.html", {
                "message": "The requested entry was not found."
            })
        markdowner = Markdown()
        htmlContent = markdowner.convert(content)
        return render(request, "wiki/displayMdPage.html", {
                "content": htmlContent,
                "name": name
            })

def editPage(request, name):    
    content = get_entry(name)
    if content is None:
        return render(request, "wiki/error.html", {
            "message": "The requested entry was not found."
        })
    return render(request, "wiki/editPage.html", {
            "content": content,
            "name": name
        })