from django.db import models
from apps.post.models import Post

from apps.user.models import CustomUser

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user} to {self.post}, comment: {self.body}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-id',)