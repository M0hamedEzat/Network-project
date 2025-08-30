
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:username>", views.profile, name="profile"),
    path("followings/", views.following_posts, name="following"),
    path("<str:username>/follow", views.follow_user, name="follow"),
    path("edit-post/<int:post_id>/", views.edit_post, name="edit_post"),
    path("like-post/<int:post_id>/", views.like_post, name="like_post"),
]
