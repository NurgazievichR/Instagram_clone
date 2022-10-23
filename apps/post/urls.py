from django.urls import path

from apps.post.views import FeaturedPosts, PostDetailView, PostListView, FeaturedPostsDetail, delete_post, HashTagPosts, update_post


urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('saved_posts/', FeaturedPosts.as_view(), name='saved_posts'),
    path('hashtags/<hashtag>', HashTagPosts.as_view(), name='hashtags'),
    path('saved_posts_detail/', FeaturedPostsDetail.as_view(), name = 'saved_posts_detail'),
    path('delete_post/<int:id>/', delete_post, name='delete_post'),
    path('post_detail_view/<int:pk>/', PostDetailView.as_view(), name='detail_post_view'),
    path('update_post/<int:id>', update_post, name='update_post')
]


