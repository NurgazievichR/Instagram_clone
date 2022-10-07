from django.db import models

from django.db import models

from apps.user.models import CustomUser


class Post(models.Model):
    title = models.CharField(max_length=355)
    owner = models.ForeignKey(CustomUser, related_name='user_posts', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField()
    views = models.IntegerField(default=0)

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


class Tag(models.Model):
    title = models.CharField('Тег', max_length=20, unique=True)
    post = models.ManyToManyField(Post,  blank=True, related_name='post_tags')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('-id',)