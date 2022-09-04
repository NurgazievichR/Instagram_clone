from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.user.models import CustomUser





class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','email','password1', 'password2']







class UserModificationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar','first_name','last_name','bio']

     