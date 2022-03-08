from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import NewBidForm, NewListingForm
from .models import User, Listing, Bid, Comment, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.all(),
        'bids': Bid.objects.all(),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# create a new listing view
def create_listing_view(request):
    # if a get request is received
    if request.method == 'GET':
        return render(request, "auctions/create_listing.html", {
            'new_listing_form': NewListingForm(),
        })
    
    # if a post method is received
    if request.method == 'POST':
        new_listing_form = NewListingForm(request.POST)
        if new_listing_form.is_valid():
            user = request.user
            title = new_listing_form.cleaned_data["title"]
            description = new_listing_form.cleaned_data["description"]
            category = new_listing_form.cleaned_data["category"]
            starting_bid = new_listing_form.cleaned_data["starting_bid"]
            image = new_listing_form.cleaned_data["image"]
            # create and save the listing and the bid
            listing = Listing.objects.create(user=user, title=title, description=description, category=category, image=image)
            starting_bid = Bid.objects.create(user=user, listing=listing, amount=starting_bid)
            return HttpResponseRedirect(reverse('index'))

# listing view
def listing_view(request, id):
    # if a get request is received
    if request.method == 'GET':
        # get the listing
        listing = Listing.objects.get(pk=id)
        bid = Bid.objects.get(listing=listing)
        return render(request, "auctions/listing.html", {
            'listing': listing,
            'bid': bid,
            'new_bid_form': NewBidForm(),
        })

# updating the bid
def bid_update(request):
    # onyl accept post requests
    if request.method == 'POST':
        new_bid_form = NewBidForm(request.POST)
        if new_bid_form.is_valid():
            new_bid = new_bid_form.cleaned_data["bid"]
            listing_id = request.POST["listing_id"]
            bid = Bid.objects.get(listing_id=listing_id)
            if new_bid > bid.amount:
                bid.amount = new_bid
                bid.save()
                return render(request, "auctions/listing.html", {
                    'listing': Listing.objects.get(pk=listing_id),
                    'bid': bid,
                    'new_bid_form': NewBidForm(),
                })

# watchlist view
def watchlist_view(request):
    if request.method == 'POST':
        listing_id = request.POST["listing_id"]
        user = request.user
        user_watchlist = Watchlist.objects.filter(user=user)
        try:
            watchlist_listing = Watchlist.objects.get(user=user, listing_id=listing_id)
            watchlist_listing.delete()
            return render(request, 'auctions/watchlist.html', {
            'watchlist': user_watchlist,
            'bids': Bid.objects.all()
            })
        except:
            Watchlist.objects.create(user=user, listing_id=listing_id)
            # after deleting or adding the listing to the watchlist
            return render(request, 'auctions/watchlist.html', {
                'watchlist': user_watchlist,
                'bids': Bid.objects.all()
            })

    elif request.method == 'GET':
        user_watchlist = Watchlist.objects.filter(user=request.user)
        return render(request, "auctions/watchlist.html", {
            'watchlist': user_watchlist,
            'bids': Bid.objects.all()
        })