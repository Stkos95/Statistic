from django import forms
from .models import Task, Category
import datetime


class AddTaskForm(forms.ModelForm):
    now = datetime.datetime.now()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория не выбрана'
        # self.fields['deadline'].empty_label = datetime.datetime.now()

    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['created', 'done']

    def is_valid(self):
        print(f'{self.errors=}')
        return super().is_valid()

