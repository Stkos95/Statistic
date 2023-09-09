from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import Group
from django import forms
from django.http import HttpResponseForbidden, JsonResponse
from django.http import HttpRequest, HttpResponse, Http404
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, TemplateView
from django.views.generic.dates import DateMixin, BaseDateListView, ArchiveIndexView
from django.contrib.auth.views import LoginView, LogoutView
import logging
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from .models import Type, Game, Actions, Records, Players
from .forms import TestForm
from django.views.generic import DetailView, CreateView, FormView

import datetime
import logging

from django.views.generic.list import ListView


class GroupRequiredMixin(AccessMixin):
    permission_denied_message = 'You have no permission for that section...'
    group_name = ''

    def get_group(self):
        return self.group_name

    def check_group(self):
        try:
            gr = Group.objects.get(name=self.get_group())
        except Group.DoesNotExists:
            return HttpResponseForbidden('Not allowed!')

        if gr in self.request.user.groups.all():
            return True
        return False







import json
class PlayersView(GroupRequiredMixin, TemplateView):
    group_name = 'Statistic'
    template_name = 'statist/players.html'


    # def _get_correct_form(self):
    #     actions = Actions.objects.filter(type=1)
    #     test_form = TestForm()
    #     for action in actions:
    #         setattr(test_form,f'{action.slug}', forms.IntegerField(label=f'{action.name}'))
    #     return test_form


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # form = self._get_correct_form()
    #     # context['form'] = form
    #     return context

    def get(self, request, *args, **kwargs):

        allow = self.check_group()
        if not allow and not self.request.user.is_staff:
            return HttpResponseForbidden(self.get_permission_denied_message())
        return super().get(request, *args, **kwargs)

    def get_template_names(self):
        if self.request.method == 'POST':
            return ['statist/statistic.html']
        else:
            return super().get_template_names()

    def post(self, request, *args, **kwargs):
        players = [value for inx, value in request.POST.items() if inx.isdigit()]
        # form = self._get_correct_form()
        actions = Actions.objects.filter(type=1)
        form = TestForm()
        for action in actions:
            form.fields[action.slug] = forms.IntegerField(label=action.name, widget=forms.NumberInput(attrs={'name': f'{action.slug}'}))
        return self.render_to_response(
            context={'players': players,
                     'form': form})
        # return  JsonResponse({'status': 'ok'})



class CountStatistic(GroupRequiredMixin,TemplateView):
    template_name = 'statistic/count.html'

    def post(self, request, *args, **kwargs):
        print(request.POST)
        return HttpResponse('Опа, отправилось!')


