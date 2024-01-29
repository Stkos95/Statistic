from django import forms
from .models import Actions, Players
from django.contrib.auth import get_user_model

class TestForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Players.objects.all())
    # name = forms.CharField(max_length=100, label='Игрок')
    # field = forms.IntegerField(min_value=0)




class InitForm(forms.Form):
    name = forms.CharField(max_length=255, label='Название игры', empty_value='Пока пусто', initial="Название игры", required=True)
    date = forms.DateField(label='Дата игры', widget=forms.DateInput(attrs={'type': 'date'}))
    url = forms.URLField(label='Ссылка для видео', initial='https://www.youtube.com/watch?v=fEoQsPvcZGs&t=264s')
    test_name = forms.IntegerField() # добавил любое поле, потому что при добавлении поля в view при оно существует только внутри этой view

    class Meta:
        widgets = {
            'date': forms.DateInput
        }


#
class ActionForm(forms.Form):
    name = forms.CharField(max_length=255)

#
# class GameTypeCreationForm(forms.Form):
#     name = forms.CharField(max_length=255, label='Группа действий:')
#
#


