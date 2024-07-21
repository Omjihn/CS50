
from django.shortcuts import render
from django.contrib import messages

def errorAndReturn(request, msgError, htmlFile):
    """
    This util funcion simply returns a render of the html file + add a error massage
    !! the page title is set to Register !!
    """
    messages.warning(request, msgError)
    return render(request, htmlFile, {
        "title": "Register"
    })