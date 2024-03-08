from django.shortcuts import render

from dataclasses import dataclass
import redis
import json
from django import forms
from django.contrib import messages

from django.http import JsonResponse

from django.views.generic import FormView, ListView, DetailView
from django.views.generic.base import TemplateView

from django.shortcuts import redirect, get_object_or_404, render

from statist.models import Actions, Players, Game, Type, Parts, RawResults, Teams




from .forms import PartsForm, CreateTypeGame, TypeFormset, PartsFormset, PlayerCreationFormset, CreateTeam





class SettingsListView(TemplateView):
    template_name = 'settings/settings.html'

class SettingsStatistic(TemplateView):
    template_name = 'settings/settings_statistic/statistic_home.html'


class TypesManageView(ListView):
    model = Type
    template_name = 'settings/settings_statistic/type_list.html'

    def get_queryset(self):
        return Type.objects.filter(user=self.request.user)




class TypesDetailView(TemplateView):
    template_name = 'settings/settings_statistic/create_type.html'

    def get(self, request, *args, **kwargs):
        current_type = None
        form_create = None
        if 'id' in self.kwargs:
            current_type = get_object_or_404(Type, pk=self.kwargs['id'])
        else:
                form_create = CreateTypeGame(prefix='type') # ОСТАНОВИЛСЯ тут, дальше, в случае создания типа, нужно создать тип, а затем добавлять в бд разделы.
        formset = TypeFormset(instance=current_type)

        context = dict()
        context['form_create'] = form_create
        context['formset'] = formset
        context['current_type'] = current_type
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        current_type = None
        form_create = CreateTypeGame(request.POST, prefix='type')
        if form_create.is_valid():
            current_type = form_create.save(commit=False)
            current_type.user_id = request.user.id
            current_type.save()

        if not current_type:
            current_type = get_object_or_404(Type, pk=self.kwargs['id'])

        form1 = TypeFormset(request.POST, instance=current_type)
        if form1.is_valid():
            parts = form1.save()
            for action in parts:
                action.type = current_type
                action.save()

        else:
            context = self.get_context_data(**kwargs)
            context['formset'] = form1
            context['current_type'] = current_type
        return self.render_to_response({})



class TeamsManageView(ListView):
    models = Teams
    template_name = 'settings/settings_teams/teams_list.html'
    context_object_name = 'teams'
    def get_queryset(self):
        return Teams.objects.filter(user=self.request.user)

class TeamDetailView(TemplateView):
    template_name = 'settings/settings_teams/team_detail.html'
    current_team = None

    def dispatch(self, request, *args, **kwargs):
        if 'pk' in self.kwargs:
            self.current_team = Teams.objects.get(pk=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formset = PlayerCreationFormset(instance=self.current_team)
        context['formset'] = formset
        context['current_team'] = self.current_team
        if not self.current_team:
            context['create_team_form'] = CreateTeam()
        return context

    def post(self, request, *args, **kwargs):
        new = False
        if not self.current_team:
            new = True
            create_team_form = CreateTeam(request.POST)

            if create_team_form.is_valid():
                self.current_team = create_team_form.save(commit=False)
                self.current_team.user = request.user
                self.current_team.save()

        formset = PlayerCreationFormset(data=request.POST, instance=self.current_team)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Список игроков успешно изменен!" if not new else 'Команда успешно создана!')

        context = self.get_context_data(**kwargs)

        return redirect('settings:detail_team', self.current_team.id)
        # return self.render_to_response(context)





def test_order(request):
    print('Пришло!!!')
    JsonResponse({'status': 'ok',})




