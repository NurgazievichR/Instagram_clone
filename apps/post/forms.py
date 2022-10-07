from operator import attrgetter
from django import forms
from apps.post.models import Post, PostImage
from django.forms import ImageField

class AddPostForm(forms.ModelForm):
    class Meta:
        fields= ['title']
        model = Post
        widgets = {
            'title': forms.TextInput(attrs={'class':'titleInput'})
        }

