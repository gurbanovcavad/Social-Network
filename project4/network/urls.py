
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("newpost/", views.new_post, name='new_post'),
    path("allposts/", views.all_posts, name='all_posts'),
    path("profile/<str:username>", views.profile, name='profile'),
    path("get/<str:username>", views.get_user_info, name='get_user_info'),
    path('follow/', views.follow, name='follow'),
    path('following/posts/<int:id>', views.following_posts, name='following'),
]
