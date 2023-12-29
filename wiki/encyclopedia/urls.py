from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("newPage", views.createEntryView.as_view(), name="newPage"),
    path("editPage/<str:title>", views.editEntryView.as_view(), name="editPage"),
    path("randomPage", views.randomPage, name="randomPage")
]
