from django import forms

from apps.save.models import Save

class SaveForm(forms.ModelForm):
    class Meta:
        model = Save
        fields = []