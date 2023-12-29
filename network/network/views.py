import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Post, User, Follow
from django.views.decorators.csrf import csrf_exempt


def index(request):
    posts = Post.objects.all().order_by("id").reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_per_page = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "posts_per_page": posts_per_page
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def post(request):
    if request.method == "POST":
            post = Post(content=request.POST["content"], user=request.user)
            post.save()
            return HttpResponseRedirect(reverse("index"))


def profile(request, username):
    posts = Post.objects.filter(user=User.objects.get(username=username)).order_by("id").reverse()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_per_page = paginator.get_page(page_number)

    following = Follow.objects.filter(user=User.objects.get(username=username))
    followers = Follow.objects.filter(user_followed=User.objects.get(username=username))

    isFollowCheck = followers.filter(user=User.objects.get(pk=request.user.id))
    if len(isFollowCheck) != 0:
        isFollow = True
    else:
        isFollow = False

    return render(request, "network/profile.html", {
        "profile": User.objects.get(username=request.user.get_username()),
        "posts_per_page": posts_per_page,
        "following": following,
        "followers":followers,
        "user": User.objects.get(username=request.user.get_username()),
        "visited_profile": User.objects.get(username=username),
        "isFollow": isFollow
    })

@login_required
def follow(request):
    user = User.objects.get(username=request.user.get_username())
    visitedProfile = User.objects.get(username=request.POST['visited_profile'])
    follow = Follow(user=user, user_followed=visitedProfile)
    follow.save()
    return HttpResponseRedirect(reverse(profile, kwargs={'username': visitedProfile.username}))

@login_required
def unfollow(request):
    user = User.objects.get(username=request.user.get_username())
    visitedProfile = User.objects.get(username=request.POST['visited_profile'])
    follow = Follow.objects.get(user=user, user_followed=visitedProfile)
    follow.delete()
    return HttpResponseRedirect(reverse(profile, kwargs={'username': visitedProfile.username}))

@login_required
def following(request):
    followings = Follow.objects.filter(user=User.objects.get(username=request.user.get_username())).values_list('user')
    if len(followings) != 0:
        posts = list(Post.objects.exclude(user__in=followings).order_by("id").reverse())
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        posts_per_page = paginator.get_page(page_number)
        return render(request, "network/following.html", {
            "posts_per_page": posts_per_page,
        })
    else:
        return render(request, "network/following.html", {
            "posts_per_page": "",
        })
    
@login_required
@csrf_exempt
def post_actions(request, id):
    post = Post.objects.get(pk=id)
    if "liked" in json.loads(request.body):
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    if "change_saved" in json.loads(request.body):
        post.content = json.loads(request.body)['content']
    post.save()
    return JsonResponse({"likes": post.likes.count()})
