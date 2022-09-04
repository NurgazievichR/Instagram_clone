from django.db import models

from apps.post.models import Post
from apps.user.models import CustomUser

class Save(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user} -- {self.post}'