import markdown2

from markdown2 import Markdown

from django.http import HttpResponse, Http404
from django.shortcuts import render

from .utils import list_entries
from .utils import get_entry

# Create your views here.

def index(request):
    entries = list_entries()
    return render(request, 'wiki/index.html', {
        'entries': entries  # Corrected the key name from "entires" to "entries"
    })

def page(request, name):
    content = get_entry(name)
    if content is None:
        return render(request, "wiki/error.html", {
            "message": "The requested entry was not found."
        })
    markdowner = Markdown()
    htmlContent = markdowner.convert(content)
    return render(request, "wiki/displayMdPage.html", {
            "content": htmlContent
        })