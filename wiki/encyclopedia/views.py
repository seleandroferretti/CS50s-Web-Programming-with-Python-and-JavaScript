import random
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View

from . import util
import markdown2
from .forms import *

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Entry page
def entry(request, title):
    entryTitle = util.get_entry(title)
    if entryTitle:
        return render(request, "encyclopedia/entryPage.html", {
            "entryTitle": title,
            "entry": markdown2.markdown(entryTitle)
        })
    else:
        return render(request, "encyclopedia/errorPage.html", {
            "entryTitle": title,
        })

# Search pages
def search(request):
    query = request.GET.get('q')
    if not query is None:
        entries = util.list_entries()
        if query in entries:
            return HttpResponseRedirect(reverse("entry", kwargs={"title": query}))
        coincidences = [entry for entry in entries if query.lower() in entry.lower()]
        if len(coincidences) == 0:
            return render(request, "encyclopedia/errorPage.html", {
                "entryTitle": query,
        })
        return render(request, "encyclopedia/index.html", {
            "entries": coincidences
        })
        
# New page
class createEntryView(View):
    def get(self, request):
        return render(request, "encyclopedia/newPage.html", {
            "newPageForm": NewPageForm()
        })
    def post(self, request):
        form = NewPageForm(request.POST)
        if form.is_valid():
            print("title: ", form.cleaned_data["title"])
            entry = util.get_entry(form.cleaned_data["title"])
            print("entry: ", entry)
            if entry is not None:
                return render(request, "encyclopedia/alreadyExistPage.html", {
                    "entryTitle": form.cleaned_data["title"],
                })
            entryTitle = "# " + form.cleaned_data["title"] + "\n"
            entryData = entryTitle + form.cleaned_data["data"]
            util.save_entry(form.cleaned_data["title"], entryData)
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })
        return HttpResponseRedirect(reverse("editPage", kwargs={"newPageForm": form}))

# Edit page
class editEntryView(View):
    def get(self, request, title):
        entry = util.get_entry(title)
        if not entry:
            return render(request, "encyclopedia/errorPage.html", {
                "entryTitle": title,
            })
        entryData = "\n".join(entry.split("\n")[1:])
        return render(request, "encyclopedia/editPage.html", {
            "editPageForm": EditPageForm(initial = {"data" : entryData}),
            "title": title
        })
    def post(self, request, title):
        form = EditPageForm(request.POST)
        if form.is_valid():
            entryTitle = "# " + title + "\n"
            entryData = entryTitle + form.cleaned_data["data"]
            util.save_entry(title, entryData)
            return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))
        return HttpResponseRedirect(reverse("editPage", kwargs={"editPageForm": form, "title": title}))

# Random page
def randomPage(request):
    entries = util.list_entries()
    entryRandomPage = random.choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={"title": entryRandomPage}))