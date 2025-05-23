from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Post, Follow
from .forms import PostForm


def index(request):
    return render(request, "network/index.html")


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
    return render(request, "network/register.html")

def new_post(request):
    if request.method == 'POST':
        try:
            body = request.POST.get('body')
            if not body: 
                raise Exception()
            post = Post(owner=request.user, body=body)
            post.save()
        except:
            return render(request, 'network/index.html', {'message': 'Something went wrong!'})
        print("success")
        return redirect(reverse('index'))
    return render(request, 'network/newpost.html')

def all_posts(request):
    posts = Post.objects.order_by('-created_at').all()
    context = {'posts': posts}
    return render(request, 'network/all_posts.html', context)

def profile(request, username):
    user = User.objects.get(username=username)
    posts = user.posts.all()
    followers = user.followers.all().count()
    following = user.following.all().count()
    is_following = Follow.objects.filter(follower=request.user, followee=user).exists()
    context = {
        'us': user,
        'posts': posts,
        'followers': followers,
        'following': following,
        'is_following': is_following,
    }
    return render(request, 'network/profile.html', context)

def get_user_info(request, username):
    user = User.objects.get(username=username)
    context = {
        'cur': request.user.id,
        'user': user.id,
        'is_following': (True if Follow.objects.filter(follower=request.user.id, followee=user) else False)
    }
    return JsonResponse(context, status=200)

@csrf_exempt
def follow(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        to_follow = data.get('follow')
        user = data.get('user')
        cur = data.get('cur')
        print(to_follow, user, cur)
        try:
            if to_follow:
                follow = Follow(follower=User.objects.get(pk=cur), followee=User.objects.get(pk=user))
                follow.save()
            else:
                Follow.objects.filter(follower=cur, followee=user).delete()
        except:
            return JsonResponse({'message': 'Something went wrong!'}, status=400)
        return JsonResponse({'message': 'Success!'}, status=200)
    return JsonResponse({'message': 'Invalid request!'}, status=400)
  
@login_required  
def following_posts(request, id):
    user = User.objects.get(pk=id)
    following = user.following.all()
    posts = []
    for i in following:
        x = User.objects.get(pk=i.followee.id)
        posts += x.posts.all()
    context = {
        "posts": posts,
    }
    return render(request, 'network/all_posts.html', context)   

@login_required
def edit_post(request, id):
    post = Post.objects.get(pk=id)
    if request.user != post.owner:
        return render(request, 'network/index.html', {'message': 'You are not allowed to edit this post!'})
    print(post)
    if request.method == 'POST':
        body = request.POST.get('body')
        if not body:
            return render(request, 'network/index.html', {'message': 'Something went wrong!'})
        post.body = body
        post.save()
        return redirect(reverse('all_posts'))
    form = PostForm(instance=post)
    print(form)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'network/edit_post.html', context)