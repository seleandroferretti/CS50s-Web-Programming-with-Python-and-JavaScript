from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from auctions.forms import NewBidForm, NewCommentForm, NewAuctionForm
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Bid, Comment, Auction, User, Watchlist

def index(request):
    category = request.GET.get('category', None)
    if category:
        auctions = Auction.objects.filter(category = category, status = 1)
    else:
        auctions = Auction.objects.filter(status = 1)
    return render(request, "auctions/index.html", {"auctions" : auctions})

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

class newAuction(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "auctions/newAuction.html", {
            "newAuctionForm": NewAuctionForm()
        })
    def post(self, request):
        form = NewAuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit = False)
            auction.author = request.user
            auction.save()
            return HttpResponseRedirect(reverse("index")) 
        return render(request, "auctions/newAuction.html", {
            "newAuctionForm": form
        })
            
class auctionPage(DetailView):
    model = Auction
    template_name = "auctions/auctionPage.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newBidForm'] = NewBidForm(initial={'id' : self.get_object().pk})
        context['newCommentForm'] = NewCommentForm()
        if self.request.user.is_authenticated:
            context['hasWatchlist'] = self.request.user.user_watchlist.filter(auction = kwargs['object']).exists()
        return context
    
class watchlist(LoginRequiredMixin, View):
    def get(self, request):
        auction = Watchlist.objects.filter(user = request.user, auction__status = 1)
        return render(request, "auctions/watchlist.html", {
            "watchlist": auction
        })

class addWatchlist(LoginRequiredMixin, View):
    def post(self, request):
        auction = Auction.objects.get(pk = request.POST["auction_id"])
        if request.POST.get('remove', False):
            Watchlist.objects.filter(user = request.user, auction = auction).delete()
        else:
            Watchlist.objects.create(user = request.user, auction = auction)
        return HttpResponseRedirect(reverse("auctionPage", kwargs={"pk":request.POST["auction_id"]}))

class categories(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "auctions/categories.html", {
            "categories": Auction.Categories.choices
        })

class newBid(LoginRequiredMixin, View):
    def post(self, request):
        actual_auction = Auction.objects.get(pk = request.POST["id"])
        actual_auction_bid = Auction.objects.get(pk = request.POST["id"]).bid
        auction_form = NewBidForm(request.POST, instance=actual_auction)
        auction = auction_form.save(commit=False)

        if (not actual_auction.auction_bid.all().exists() and actual_auction_bid==auction.bid) or (actual_auction_bid < auction.bid):
            auction.save()
            bid = Bid(user=request.user, auction=auction, bid=auction.bid)
            bid.save()
            messages.success(request, "Your bid was saved successfully!", extra_tags='success')
            return HttpResponseRedirect(reverse("auctionPage", kwargs={"pk":request.POST["id"]}))
        messages.error(request, "Your bid must be greater than the current one!", extra_tags='error')
        return HttpResponseRedirect(reverse("auctionPage", kwargs={"pk":request.POST["id"]}))

class newComment(LoginRequiredMixin, View):
    def post(self, request, pk):
        auction = Auction.objects.get(pk = pk)
        comment = NewCommentForm(request.POST)
        comment_object = comment.save(commit=False)
        comment_object.user = request.user
        comment_object.auction = auction
        comment_object.save()
        return HttpResponseRedirect(reverse("auctionPage", kwargs={"pk":pk}))

class finishAuction(LoginRequiredMixin, View):
    def post(self, request, pk):
        auction = Auction.objects.get(pk = pk)
        auction.status=False
        auction.save()
        return HttpResponseRedirect(reverse("auctionPage", kwargs={"pk":pk}))