from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    avatar = models.ImageField(upload_to='users/', blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)
    last_activity= models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Activity(models.Model):
    today = models.IntegerField(default=0)
    all_time = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)


    def __str__(self) -> str:
        return f'{self.date}'

    class Meta:
        verbose_name = 'Активность'
        verbose_name_plural = 'Активность'


