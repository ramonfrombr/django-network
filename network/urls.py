
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/<str:username>/<int:page_number>", views.profile_post_page, name="profile_post_page"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("unfollow/<str:username>", views.unfollow, name="unfollow"),
    path("posts_following", views.posts_following, name="posts_following"),
    path("like/<int:post_id>", views.like, name="like"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("page/<int:page_number>", views.page, name="page"),
]
