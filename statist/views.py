from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django import forms
from django.http import HttpResponseForbidden, JsonResponse
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import AccessMixin
from .models import Actions, Players, Results
from .forms import TestForm
from statist.serialization1 import serialisation1
from django.forms import formset_factory, BaseFormSet
# from statist.db.db import db_processing
from .count import accumulate_statistic
from django.contrib.auth.views import LoginView
import redis
from .statistic_to_image import OurTeamImage
from .tasks import add

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


r = redis.Redis(host='172.26.0.2', port=6379, decode_responses=True)


class CountStatisticView(GroupRequiredMixin, TemplateView):
    template_name = 'statist/statistic.html'

    def get(self, request, *args, **kwargs):
        players = Players.objects.all()
        action_by_category = {
            '1': [],
            '2': []
        }
        actions = Actions.objects.filter(type=1)
        for i in actions:
            if i.name not in seldom_actions:
                action_by_category['1'].append(i)
            else:
                action_by_category['2'].append(i)

        return self.render_to_response(
            context={
                'actions_by_category': action_by_category,
                'players': players,
                'actions': actions,
                'statistic_type': 1})


from pprint import pprint
import os

class ResultStatisticView(GroupRequiredMixin, TemplateView):
    template_name = 'statistic/count.html'
    status = ('success', 'fail')

    def get(self, request, *args, **kwargs):
        return HttpResponse('Опа, отправилось!')

    def post(self, request, *args, **kwargs):
        game_name = request.POST.get('game-name')
        game_date = request.POST.get('game-date')
        players = Players.objects.all()
        actions = Actions.objects.all()
        halfs_players = r.keys()
        result = {}
        final = {}
        for key in halfs_players:

            half, player_id = key.split(':')
            player = [i for i in players if i.id == int(player_id)][0]
            result.setdefault(player.name, {'photo': {}, 'actions': {}})
            result[player.name]['photo'] = player.photo
            data = r.hgetall(key)
            for action in actions:
                result[player.name]['actions'].setdefault(action.name, {})
                value = {i: data[f'{action.slug}-{i}'] for i in self.status}
                result[player.name]['actions'][action.name][half] = value
                # for i in value:
                #     Results.objects.create(
                #     player=player,
                #     game=game_name,
                #     action=action,
                #     status=i,
                #     value=value[i])
        for player in result:
            d = accumulate_statistic(result[player]['actions'])
            # print(player, d)
            image = OurTeamImage()
            image.make_header(game_name, game_date, player, result[player]['photo'])
            image.put_statistic(d)
            image.show()






        return JsonResponse({'status': 'hello'})


def get_any_data(request, *args):
    data = json.load(request)
    return (data.get(i) for i in args)


def initial_players(request):
    data = json.load(request)

    keys = (f'1:{data["player_id"]}', f'2:{data["player_id"]}')
    mapping = {action: 0 for action in data.get('actions')}
    result = {}
    data_exist = False
    for half, key in enumerate(keys, start=1):
        data_half = r.hgetall(key)
        if data_half:
            data_exist = True
            break
        else:
            r.hset(key, mapping=mapping)
    if data_exist:
        return JsonResponse({'status': 'exist'})

    return JsonResponse({'status': 'ok'})


def count_statistic(request):
    half, player_id, action = get_any_data(request, 'half', 'player_id', 'action')
    key = f'{half}:{player_id}'
    r.hincrby(key, action, 1)
    new_value = r.hget(key, action)
    print(r.hget(key, action))

    return JsonResponse({'response': 'ok',
                         'value': new_value})


def get_player_data(request):
    half, player_id = get_any_data(request, 'half', 'player_id')
    key = f'{half}:{player_id}'

    res = r.hgetall(key)

    response = {
        'status': 'ok',
        'data': res
    }

    return JsonResponse(response)


def celery_test(request):
    add.apply_async()
    return JsonResponse({'response': 'ok'})
