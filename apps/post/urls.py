from django.urls import path

from apps.post.views import PostListView

urlpatterns = [
    path('', PostListView.as_view(), name='index')
]