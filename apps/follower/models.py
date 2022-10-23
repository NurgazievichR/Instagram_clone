from django.db import models

from django.db import models

from apps.user.models import CustomUser
 

class Follower(models.Model):
    to_user = models.ForeignKey(CustomUser, related_name='subscribers', on_delete=models.CASCADE)
    from_user = models.ForeignKey(CustomUser, related_name="subscribs", on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return f"Subscribe {self.create_at} from {self.from_user} to {self.to_user}"

    class Meta:
        ordering = ('-create_at',)  
