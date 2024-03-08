from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import Actions, Players, Type, Teams
from django.contrib.auth import get_user_model

class TestForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Players.objects.all())
    # name = forms.CharField(max_length=100, label='Игрок')
    # field = forms.IntegerField(min_value=0)




class InitForm(forms.Form):
    name = forms.CharField(max_length=255, label='Название игры', empty_value='Пока пусто', initial="Название игры", required=True)
    date = forms.DateField(label='Дата игры', widget=forms.DateInput(attrs={'type': 'date'}))
    url = forms.URLField(label='Ссылка для видео', initial='https://www.youtube.com/watch?v=fEoQsPvcZGs&t=264s')
    # test_name = forms.IntegerField() # добавил любое поле, потому что при добавлении поля в view при оно существует только внутри этой view
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teams'] = forms.ChoiceField(choices=Teams.objects.values_list('id', 'name').filter(user=request.user),
                                             label='Выберите команду:')
        self.fields['test_name'] = forms.ChoiceField(choices=Type.objects.values_list('id', 'name').filter(Q(user=request.user.id) | Q(user=None)))








    class Meta:
        widgets = {
            'date': forms.DateInput
        }


#
class ActionForm(forms.Form):
    name = forms.CharField(max_length=255)









#
class GameTypeCreationForm(forms.ModelForm):
    # name = forms.CharField(max_length=255, label='Группа действий:')

    class Meta:
        model = Actions
        fields = '__all__'

        # widgets = {
        #     'name': forms.TextInput(
        #         attrs={
        #             'required': 'true'
        #         }
        #     ),
        #
        # }

    # def clean(self):
    #     name = self.cleaned_data.get('name', None)
    #     if not name:
    #         print('not a name')
    #
    # def clean_name(self):
    #     name = self.cleaned_data.get('name', None)
    #     print(f'{name=}')
    #     if not name:
    #         print('not name')



    # def add_error(self, field, error):






