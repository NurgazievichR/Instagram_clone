from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from apps.user.models import CustomUser





class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','email','password1', 'password2']







class UserModificationForm(forms.ModelForm):
    # username = forms.CharField(widget=forms.TextInput(), required=False, max_length=50)

    class Meta:
        model = CustomUser
        fields = ['avatar','first_name','last_name','bio']



        