from django import forms 

from apps.follower.models import Follower

class FollowerForm(forms.ModelForm):
    class Meta:
        fields = []
        model = Follower