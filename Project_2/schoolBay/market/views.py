from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Comment, Listing, Bid

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "market/index.html", {
        'title' : 'Home - SchoolBay',
        "user": request.user.username,
        "listings": Listing.objects.all()
    })

def addListing(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to add a listing.")
        return HttpResponseRedirect(reverse("login"))

    if request.method == 'POST':
        user = request.user
        title = request.POST['title']
        description = request.POST['description']
        starting_price = request.POST['starting_price']

        if not title or not description or not starting_price:
            messages.error(request, 'All fields are required.')
            return render(request, 'market/createListing.html' , {
                'title' : 'Create Listing'
            })
        
        try:
            starting_price = float(starting_price)
        except ValueError:
            messages.error(request, "Invalid price.")
            return render(request, 'market/createListing.html' , {
                'title' : 'Create Listing'
            })

        listing = Listing(title=title, user=user, description=description, starting_price=starting_price)
        listing.save()
        return redirect(f"/listing/{listing.id}/")

    return render(request, 'market/createListing.html', {
        'title' : 'Create listing'
    })

def showListing(request, id):
    listing = get_object_or_404(Listing, id=id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment = request.POST['comment']
            if len(comment.strip()) != 0:
                comment = Comment(user=request.user, listing=listing, content=comment)
                comment.save()
            else:
                messages.error(request, 'Error you comment musn\'t contain only whitespaces.')
                return HttpResponseRedirect(reverse('showListing', args=[id]))


    return render(request, "market/showListing.html" , {
        'listing' : listing,
        'comments': listing.comment.all(),
        'title' : listing.title + " - SchoolBay"
    })