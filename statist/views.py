from django.contrib.auth.models import Group
from django import forms
from django.http import HttpResponseForbidden, JsonResponse
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import AccessMixin
from .models import Actions, Players
from .forms import TestForm
from statist.serialization1 import serialisation1
from django.forms import formset_factory, BaseFormSet
from statist.db.db import db_processing

import json


# class TestBaseFormSet(BaseFormSet):
#     def add_fields(self, form, index):
#         super().add_fields(form, index)
#         actions = Actions.objects.filter(type=1)
#         for action in actions:
#             form.fields[action.slug] = forms.IntegerField(label=action.name,min_value=0)


seldom_actions = ['Обводка', 'Перехват', 'Отбор']

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


class PlayersView(GroupRequiredMixin, TemplateView):
    group_name = 'Statistic'
    template_name = 'statist/players.html'

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



class CountStatisticView(GroupRequiredMixin, TemplateView):
    template_name = 'statist/statistic.html'

    def get(self, request, *args, **kwargs):
        players = Players.objects.all()
        action_by_category = {
            '1': [],
            '2': []
        }

        initial = []
        for player in players:
            initial.append({'name': player})
        TestFormSet = formset_factory(TestForm)

        formset = TestFormSet(initial=initial)
        actions = Actions.objects.filter(type=1)
        for i in actions:
            if i.name not in seldom_actions:
                action_by_category['1'].append(i)
            else:
                action_by_category['2'].append(i)

        return self.render_to_response(
            context={'formset': formset,
                     'actions_by_category': action_by_category,
                     'players': players,
                     'actions': actions,
                     'statistic_type': 1})





class ResultStatisticView(GroupRequiredMixin,TemplateView):
    template_name = 'statistic/count.html'

    def get(self, request, *args, **kwargs):

        return HttpResponse('Опа, отправилось!')



    def post(self, request, *args, **kwargs):
        print(request.POST)
        db = db_processing()

        data = json.load(request)
        res = db.test.update_one(data, {'$inc':{'value': 1}}, upsert=True)
        print(res)



        # print(request.POST)
        # data = dict(request.POST)

        # players_statistic_json = serialisation1(data)
        # print(players_statistic_json)

        return JsonResponse({'status': 'OK'})


def ajax(request):

    data = json.load(request)
    player_id = data['player_id']
    half = data['half']

    db = db_processing()
    res = db.test.find({'player_id': player_id,
                  'half': half
    })
    print(res)
    return JsonResponse(res)
