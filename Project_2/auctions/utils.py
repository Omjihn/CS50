
from django.shortcuts import render
from django.contrib import messages
import requests

def is_url_image(image_url):
    try:
        response = requests.head(image_url)
        if response.status_code == 200 and response.headers['Content-Type'].startswith('image/'):
            return True
        else:
           return False
    except requests.exceptions.RequestException:
        return False

def errorAndReturn(request, msgError, htmlFile):
    """
    This util funcion simply returns a render of the html file + add a error massage
    !! the page title is set to Register !!
    """
    messages.warning(request, msgError)
    return render(request, htmlFile, {
        "title": "Register"
    })
