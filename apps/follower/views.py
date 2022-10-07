from django.shortcuts import render
from django.views.generic import TemplateView

from apps.follower.models import Follower
from apps.user.utils import get_id_by_username
from apps.post.mixins import SearchMixin

class FollowersView(SearchMixin,TemplateView):
    template_name = 'users_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Followers'
        try:
            followers = Follower.objects.filter(to_user=get_id_by_username(kwargs['username']))
            context['followers'] = followers
        except Exception as _ex:
            print(_ex)
            context['followers'] = None

        return context


class FollowingsView(SearchMixin,TemplateView):
    template_name = 'users_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Followings'
        try:
            followings = Follower.objects.filter(from_user=get_id_by_username(kwargs['username']))
            context['followings'] = followings
        except Exception as _ex:
            print(_ex)
            context['followings'] = None
        return context
        