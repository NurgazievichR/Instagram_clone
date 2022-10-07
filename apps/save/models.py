from django.db import models

from apps.post.models import Post
from apps.user.models import CustomUser

class Save(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_saved')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user} -- {self.post}'

    class Meta:
        verbose_name = 'Сохраненный'
        verbose_name_plural = 'Сохранённые'
        ordering = ('-id',)