from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

class Auction(models.Model):
    class Categories(models.TextChoices):
        APPLIANCES = '1','Appliances'
        HYGIENE = '2','Hygiene'

    title = models.CharField(max_length=80)
    description = models.CharField(max_length=250)
    bid = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    picture_url = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=datetime.now)
    status = models.BooleanField(default=True)
    category = models.TextField(choices=Categories.choices)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_auction")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer_auction", blank=True, null=True)

    def get_last_bid(self):
        bid = self.auction_bid.all()
        if bid.exists():
            return bid.first()
        return {}

class Watchlist(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="watched_auction")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_bid")
    created_date = models.DateTimeField(default=datetime.now)
    bid = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")

    class Meta:
        ordering = ("-created_date",)

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_comment")
    created_date = models.DateTimeField(default=datetime.now)
    comment = models.CharField(max_length=300, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")