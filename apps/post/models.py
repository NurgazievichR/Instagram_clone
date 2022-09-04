from django.db import models

from django.db import models

from apps.user.models import CustomUser


class Post(models.Model):
    title = models.CharField(max_length=4096)
    owner = models.ForeignKey(CustomUser, related_name='user_posts', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.title}---{self.owner.username}"

    class Meta:
        ordering = ('-create_at',)


class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='post_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users_post/')

    def __str__(self):
        return f"{self.post.title}---{self.post.owner.username}----{self.pk}"

    class Meta:
        ordering = ("id",)
