from django import forms
from .models import Actions, Players

class TestForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Players.objects.all())
    # name = forms.CharField(max_length=100, label='Игрок')
    # field = forms.IntegerField(min_value=0)



class InitForm(forms.Form):
    name = forms.CharField(max_length=255, label='Название игры', empty_value='Пока пусто', initial="Название игры", required=True)
    date = forms.DateField(label='Дата игры', widget=forms.DateInput(attrs={'type': 'date'}))
    url = forms.URLField(label='Ссылка для видео', initial='https://www.youtube.com/watch?v=fEoQsPvcZGs&t=264s')

    class Meta:
        widgets = {
            'date': forms.DateInput
        }




