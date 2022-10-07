from django.db import models

from apps.post.models import Post
from apps.user.models import CustomUser

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    def __str__(self) -> str:
        return f'{self.user} to {self.post}'    