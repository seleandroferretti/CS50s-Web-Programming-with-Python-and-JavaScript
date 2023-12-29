from django.contrib import admin

# Register your models here.
from auctions.models import User, Auction, Watchlist, Bid, Comment

admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Watchlist)
admin.site.register(Bid)
admin.site.register(Comment)