from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.contrib.auth.models import User, Permission

from .models import Task, Category
import datetime


class AddTaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория не выбрана'
        # self.fields['deadline'].empty_label = datetime.datetime.now()

    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['created', 'done', 'user']

    def is_valid(self):
        print(f'{self.errors=}')
        return super().is_valid()


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        fields = ['username', 'email', 'password1', 'password2']
        model = User


