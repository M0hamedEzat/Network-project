from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.forms import ModelForm
from .models import User, Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'What\'s on your mind?'})
        }
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if not content:
            raise forms.ValidationError("Content is required.")
        return content

def index(request):
    form = PostForm()
    if request.method == "POST":
        which = request.POST.get("which")
        if which == "new_post":
            form = PostForm(request.POST)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.author = request.user
                new_post.save()
                return HttpResponseRedirect(reverse("index"))
    all_posts = Post.objects.all()
    return render(request, "network/index.html", {
        "form": form,
        "all_posts": all_posts
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


def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_posts = user.posts.all()
    return render(request, "network/profile.html", {
        "profile_user": user,
        "user_posts": user_posts,
    })

def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user.is_authenticated:
        if user_to_follow in request.user.following.all():
            request.user.following.remove(user_to_follow)
            user_to_follow.followers.remove(request.user)
        else:
            request.user.following.add(user_to_follow)
            user_to_follow.followers.add(request.user)
    return HttpResponseRedirect(reverse("profile", args=[username]))