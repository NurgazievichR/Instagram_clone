from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    avatar = models.ImageField(upload_to='users/', blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


