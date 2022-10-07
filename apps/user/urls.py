from django.urls import path
from django.views.generic import RedirectView

from apps.user.views import LogoutUser, ProfileDetailView, ProfilePostsView, RegisterUser, LoginUser, UpdateUser, addPost

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('editmyprofile/', UpdateUser.as_view(), name='editmyprofile'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile'),
    path('addpost/', addPost, name='add_post'),
    path('detail_posts/<username>/', ProfilePostsView.as_view(), name='profileDetailPosts')
]