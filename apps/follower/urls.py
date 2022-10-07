from django.urls import path

from apps.follower.views import FollowersView, FollowingsView

urlpatterns = [
    path('followers/<username>/', FollowersView.as_view(), name='followers'),
    path('followings/<username>/', FollowingsView.as_view(), name='followings'),
]