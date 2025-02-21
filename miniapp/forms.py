from django import forms
from .models import bag

class Addforms(forms.ModelForm):
    class Meta:
        model=bag
        fields='__all__'