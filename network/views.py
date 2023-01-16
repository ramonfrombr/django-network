from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, UserFollowing, Like
from django.http import JsonResponse
import json
from django.core.paginator import Paginator


class NewPostForm(forms.Form):
    content = forms.CharField(max_length=500, label="", widget=forms.Textarea(attrs={'rows': 2, 'placeholder': "Write something..."}))


def index(request):

    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            newPost = Post(content=form.cleaned_data['content'], user=request.user)
            newPost.save()

    return HttpResponseRedirect(reverse('page', args=(1,)))


def page(request, page_number):

    form = NewPostForm()

    posts = Post.objects.all().order_by('-created_at')

    postlist = []

    for post in posts:
        postObj = {"post": post, "user_liked": False}
        for like in list(post.likes.all()):
            if request.user == like.user:
                postObj["user_liked"] = True
                break   
        postlist.append(postObj)

    paginator = Paginator(postlist, 10)

    return render(request, "network/index.html",{"form": form,"posts": paginator.page(page_number), "num_pages": range(paginator.num_pages)})


def following(request):
    return HttpResponseRedirect(reverse('following_post_page', args=(1,)))


def following_post_page(request, page_number):

    followers = [follow.following_user for follow in list(request.user.following.all())]

    posts = Post.objects.filter(user__in=followers).order_by('-created_at')

    postlist = []

    for post in posts:
        postObj = {"post": post, "user_liked": False}
        for like in list(post.likes.all()):
            if request.user == like.user:
                postObj["user_liked"] = True
                break   
        postlist.append(postObj)

    paginator = Paginator(postlist, 10)

    return render(request, "network/following.html",{"posts": paginator.page(page_number), "num_pages": range(paginator.num_pages)})


def profile(request, username):
    return HttpResponseRedirect(reverse('profile_post_page', args=(username,1,)))


def profile_post_page(request, username, page_number):

    user = User.objects.get(username=username)

    if user:

        followers = [follow.user for follow in list(user.followers.all())]

        postlist = []

        for post in user.posts.all().order_by('-created_at'):
            postObj = {"post": post, "user_liked": False}
            for like in list(post.likes.all()):
                if request.user == like.user:
                    postObj["user_liked"] = True
                    break   
            postlist.append(postObj)

        paginator = Paginator(postlist, 10)

        return render(request, "network/profile.html", {"profile_user": user, "followers": followers, "posts": paginator.page(page_number), "num_pages": range(paginator.num_pages)})
    else:
        print("ERROR: NO USER")# ERROR
        return HttpResponseRedirect(reverse('index'))


@csrf_exempt
def like(request, post_id):

    post = Post.objects.get(id=post_id)

    like = Like.objects.filter(post=post,user=request.user)

    if like:
        print(like[0])
        like[0].delete()

        return JsonResponse({
            "action": "unlike"
        }, status=200)
    else:
        like = Like(post=post, user=request.user)
        like.save()

        return JsonResponse({
            "action": "like"
        }, status=200)


@csrf_exempt
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if post.user == request.user:

        json_string = request.body.decode('utf8').replace("'", '"')
        data = json.loads(json_string)
        post = Post.objects.get(id=post_id)
        post.content = data["content"]
        post.save()

        return JsonResponse({
                "status": "success",
                "message": "Post editted successfully."
            }, status=200)
    else:
        return JsonResponse(
            data={
                "status": "error",
                "message": "User is not the post author."
            }, status=403
        )


def follow(request, username):
    following_user = User.objects.get(username=username)
    follow = UserFollowing.objects.filter(user=request.user, following_user=following_user)
    if not follow:
        follow = UserFollowing(user=request.user, following_user=following_user)
        follow.save()
    return HttpResponseRedirect(reverse('profile', args=(username,)))


def unfollow(request, username):
    following_user = User.objects.get(username=username)
    follow = UserFollowing.objects.filter(user=request.user, following_user=following_user)[0]
    follow.delete()
    return HttpResponseRedirect(reverse('profile', args=(username,)))


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

