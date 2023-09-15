from django import forms
from .models import Actions

class TestForm(forms.Form):
    name = forms.CharField(max_length=100, label='Игрок')
    # field = forms.IntegerField(min_value=0)



