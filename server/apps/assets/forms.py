from django import forms
from apps.assets.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['source',]
        widgets = {
            'source': forms.ClearableFileInput(attrs={'multiple': True, 'class': 'file--selector--input'})
        }
