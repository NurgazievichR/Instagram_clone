from django.db import models
from django.core.validators import FileExtensionValidator

from apps.user.models import CustomUser

class Story(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = 'user_stories' )
    create_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='story_file', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov' ,'jpg', 'jpeg'])])


    def __str__(self) -> str:
        return f'Stories -- {self.user}' 

    class Meta:
        ordering = ('create_at',)
