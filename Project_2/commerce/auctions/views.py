from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError

from decimal import Decimal, InvalidOperation

from .utils import errorAndReturn, is_url_image
from .models import Comment, Listing, Bid, Watchlist

# Create your views here.

###     AUCTION     ###

def index(request):
	if request.GET.get('school_level'):
		try:
			listings = Listing.objects.filter(level=request.GET.get('school_level'))
		except:
			listings = None
	else:
		listings = Listing.objects.all()
	return render(request, "auctions/index.html", {
		'title' : 'Home - SchoolBay',
		"user": request.user,
		"listings": listings
	})

def addListing(request):
	if not request.user.is_authenticated:
		messages.warning(request, "You must be logged in to add a listing.")
		return HttpResponseRedirect(reverse("login"))

	if request.method == 'POST':
		user = request.user
		title = request.POST['title']
		description = request.POST['description']
		picture = request.POST['picture']
		level = request.POST['level']

		try:
			starting_price = float(request.POST['starting_price'])
		except ValueError:
			messages.error(request, "Invalid price.")
			return render(request, 'auctions/createListing.html' , {
				'title' : 'Create Listing'
			})

		if not title or not description or not starting_price:
			messages.error(request, 'All fields are required.')
			return render(request, 'auctions/createListing.html' , {
				'title' : 'Create Listing'
			})
		print(picture)
		if not is_url_image(picture):
			picture = ""
		listing = Listing(title=title, user=user, description=description, starting_price=starting_price, current_price=starting_price, picture=picture, level=level)
		listing.save()
		return redirect(f"/listing/{listing.id}/")

	return render(request, 'auctions/createListing.html', {
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


	return render(request, "auctions/showListing.html" , {
		'watchlist_status' : watchlist_status,
		'bids' : bids,
		'listing' : listing,
		'comments': listing.comment.all(),
		'title' : listing.title + " - SchoolBay"
	})

def addBid(request, id):
	listing = get_object_or_404(Listing, id=id)

	if listing.closed:
		messages.error(request, "This listing has been closed and cannot accept new bids.")
		return redirect(f"/listing/{listing.id}/")

	if not request.user.is_authenticated:
		messages.warning(request, 'You must be logged in to add a bid.')
		return redirect(reverse("login"))
	
	if request.user.id == listing.user.id:
		messages.error(request, 'You can\'t add a bid on your own listing.')
		return render(request, 'auctions/createBid.html', {
			'listing': listing,
			'title': "Bid - SchoolBay"
		})

	if request.method == 'POST':
		
		description = request.POST['description']

		if not description or len(description.strip()) == 0:
			messages.error(request, 'You must add a comment.')
			return render(request, 'auctions/createBid.html', {
				'listing': listing,
				'title': "Bid - SchoolBay"
			})

		try:
			price = Decimal(request.POST['price'])
			price = round(Decimal(price), 2)
			print(f"Rounded :{price} | current price {listing.current_price}")
		except InvalidOperation:
			messages.error(request, "Invalid price.")
			return render(request, 'auctions/createBid.html', {
				'listing': listing,
				'title': 'Bid - SchoolBay'
			})

		if price >= 1000000000000000000:
			messages.error(request, "Invalid price.")
			return render(request, 'auctions/createBid.html', {
				'listing': listing,
				'title': 'Bid - SchoolBay'
			})

		if price <= listing.current_price:
			messages.error(request, "The price must be greater than the current bid.")
			return render(request, 'auctions/createBid.html', {
				'listing': listing,
				'title': 'Bid - SchoolBay'
			})

		bid = Bid(user=request.user, listing=listing, price=price, content=description)
		bid.save()

		listing.current_price = price
		listing.save()
		
		messages.success(request, 'Your bid has been added.')
		return redirect(f"/listing/{listing.id}/")

	return render(request, 'auctions/createBid.html', {
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
	return render(request, 'auctions/watchlist.html', {
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

def searchCategory(request):
	return render(request, 'auctions/searchCategory.html', {
		'title': 'Search - SchoolBay'
	})

###     USER        ###

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
		return HttpResponseRedirect(reverse("index"))

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		else:
			messages.warning(request, 'Invalid login or password.')
			return render(request, "auctions/loginForm.html", {
		"title": "Login"
	})

	return render(request, "auctions/loginForm.html", {
		"title": "Login"
	})

def register_view(request):
	"""
	Django view who render the register page and haddle the register POST who create the user
	"""
	if request.method == "POST":
		username = request.POST.get('username')
		
		if username != request.POST.get('username').strip():
			return errorAndReturn(request, 'Username can\'t contain whitespaces.', "auctions/registerForm.html")
		
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		if password1 != password2:
			return errorAndReturn(request, 'Passwords do not match.', "auctions/registerForm.html")
		try:
			user = User.objects.create_user(username, None,  password1)
			user.save()
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		except IntegrityError:
			return errorAndReturn(request, 'Username already taken.', "auctions/registerForm.html")
		except ValueError as ve:
			return errorAndReturn(request, str(ve), "auctions/registerForm.html")
	return render(request, "auctions/registerForm.html", {
		'title': 'Register'
	})
