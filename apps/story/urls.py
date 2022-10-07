from django.urls import path

from apps.story.views import ImageOrVideo, addVideoStory, StoriesView

urlpatterns = [
    path('story/<str:username>/', StoriesView.as_view(), name='story'),
    path('add-video-story/', addVideoStory, name='add_video_story'),
]