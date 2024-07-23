from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Comment, Listing, Bid, Watchlist

# Create your views here.

def index(request):
    return render(request, "market/index.html", {
        'title' : 'Home - SchoolBay',
        "user": request.user,
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
        picture = request.FILES.get('picture')
        level = request.POST['level']

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

        listing = Listing(title=title, user=user, description=description, starting_price=starting_price, current_price=starting_price, picture=picture, level=level)
        listing.save()
        return redirect(f"/listing/{listing.id}/")

    return render(request, 'market/createListing.html', {
        'title' : 'Create listing'
    })

def showListing(request, id):
    listing = get_object_or_404(Listing, id=id)
    bids = Bid.objects.filter(listing=listing).order_by('-creation_date')
    if request.user.is_authenticated and Watchlist.objects.filter(user=request.user, listing=listing).exists():
        watchlist_status = 'Remove From Watchlist'
    else:
        watchlist_status = 'Add To Watchlist'
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment = request.POST['comment']
            if len(comment.strip()) != 0:
                comment = Comment(user=request.user, listing=listing, content=comment)
                comment.save()
            else:
                messages.error(request, 'Error you comment musn\'t contain only whitespaces.')
                return HttpResponseRedirect(reverse('showListing', args=[id]))
        else:
            messages.warning(request, 'You must be logged in to add a comment.')


    return render(request, "market/showListing.html" , {
        'watchlist_status' : watchlist_status,
        'bids' : bids,
        'listing' : listing,
        'comments': listing.comment.all(),
        'title' : listing.title + " - SchoolBay"
    })

def addBid(request, id):
    listing = get_object_or_404(Listing, id=id)

    # Check if the listing is closed
    if listing.closed:
        messages.error(request, "This listing has been closed and cannot accept new bids.")
        return redirect(f"/listing/{listing.id}/")

    if not request.user.is_authenticated:
        messages.warning(request, 'You must be logged in to add a bid.')
        return redirect(reverse("login"))
    
    if request.user.id == listing.user.id:
        messages.error(request, 'You can\'t add a bid on you\'r own listing.')
        return render(request, 'market/createBid.html', {
            'listing': listing,
            'title': "Bid - SchoolBay"
        })

    if request.method == 'POST':
        price = request.POST['price']
        description = request.POST['description']

        # Validate description
        if not description or len(description.strip()) == 0:
            messages.error(request, 'You must add a comment.')
            return render(request, 'market/createBid.html', {
                'listing': listing,
                'title': "Bid - SchoolBay"
            })

        # Validate price
        try:
            float(price)
        except ValueError:
            messages.error(request, "Invalid price.")
            return render(request, 'market/createBid.html', {
                'listing': listing,
                'title': 'Bid - SchoolBay'
            })

        if float(price) <= listing.current_price:
            messages.error(request, "The price must be greater than the current bid.")
            return render(request, 'market/createBid.html', {
                'listing': listing,
                'title': 'Bid - SchoolBay'
            })

        # Create and save the new bid
        bid = Bid(user=request.user, listing=listing, price=price, content=description)
        bid.save()
        
        # Update the listing's current price
        listing.current_price = price
        listing.save()
        
        messages.success(request, 'Your bid has been added.')
        return redirect(f"/listing/{listing.id}/")

    return render(request, 'market/createBid.html', {
        'listing': listing,
        'title': "Bid - SchoolBay"
    })

def watchlistSwitch(request, id):
    listing = get_object_or_404(Listing, id=id)
    if not request.user.is_authenticated:
        messages.warning(request, 'You must be logged in to add a listing to your watchlist.')
        return HttpResponseRedirect(reverse("login"))
    try:
        watchlist = Watchlist.objects.get(user=request.user, listing=listing)
        watchlist.delete()
    except:
        watchlist = Watchlist(user=request.user, listing=listing)
        watchlist.save()
    return HttpResponseRedirect(reverse('showListing', args=[id]))

def watchlist(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'You must be logged in to access your watchlist.')
        return HttpResponseRedirect(reverse("login"))
    watchlist_items = Watchlist.objects.filter(user=request.user).select_related('listing')
    return render(request, 'market/watchlist.html', {
        'title' : 'Watchlist - SchoolBay',
        'watchlist_items' : watchlist_items
    })

def close_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    if request.method == 'POST':
        if request.user == listing.user and not listing.closed:
            listing.closed = True
            listing.save()
            messages.success(request, 'Listing has been closed.')
        else:
            messages.error(request, 'You are not authorized to close this listing or it is already closed.')
    
    return redirect(reverse('showListing', args=[listing_id]))