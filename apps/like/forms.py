from django import forms

from apps.like.models import Like

class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = []