from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from apps.user.views import LogoutUser, ProfileDetailView, ProfilePostsView, RegisterUser, LoginUser, UpdateUser, addPost

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('editmyprofile/', UpdateUser.as_view(), name='editmyprofile'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile'),
    path('addpost/', addPost, name='add_post'),
    path('detail_posts/<username>/', ProfilePostsView.as_view(), name='profileDetailPosts'),
    path('password/', auth_views.PasswordChangeView.as_view(template_name='password/password_change.html', success_url = reverse_lazy('index')), name='password_change')
    
]

