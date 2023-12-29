from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newAuction", views.newAuction.as_view(), name="newAuction"),
    path("auctionPage/<int:pk>", views.auctionPage.as_view(), name="auctionPage"),
    path("watchlist", views.watchlist.as_view(), name="watchlist"),
    path("categories", views.categories.as_view(), name="categories"),
    path("newBid", views.newBid.as_view(), name="newBid"),
    path("addWatchlist", views.addWatchlist.as_view(), name="addWatchlist"),
    path("auctionPage/<int:pk>/newComment", views.newComment.as_view(), name="newComment"),
    path("auctionPage/<int:pk>/finishAuction", views.finishAuction.as_view(), name="finishAuction"),
]
