from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django import forms
from django.http import HttpResponseForbidden, JsonResponse
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import AccessMixin
from .models import Actions, Players, ResultsJson
from .forms import TestForm
from statist.serialization1 import serialisation1
from django.forms import formset_factory, BaseFormSet
# from statist.db.db import db_processing
from .count import accumulate_statistic
from django.contrib.auth.views import LoginView
import redis
from .statistic_to_image import OurTeamImage
# from .tasks import add
from io import BytesIO
import json
from PIL import Image, ImageDraw, ImageFont, ImageOps

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


# from pprint import pprint
# import os
# from dataclasses import dataclass
#
#
#
# @dataclass
# class MatchInfo:
#     game_name: str
#     game_date: str
#     players: list
#     actions: list
#
# def test(match_info: MatchInfo):
#     status = ('success', 'fail')
#     halfs_players = r.keys()
#     players_list = set(map(lambda x: x.split(':')[1], halfs_players))
#     for pl in players_list:
#         result = {}
#         player = [i for i in match_info.players if i.id == int(pl)][0]
#         halfs = [key for key in halfs_players if key.endswith(f':{pl}')]
#         result['photo'] = player.photo
#         result['actions'] = {}
#         for h in halfs:
#             half = h.split(':')[0]
#             data = r.hgetall(h)
#             for action in match_info.actions:
#                 if action.name not in result['actions']:
#                     result['actions'].setdefault(action.name, {})
#                 value = {i: data[f'{action.slug}-{i}'] for i in status}
#                 result['actions'][action.name][half] = value
#         yield result




from tg_bot.tasks import test1, final_task
from .tasks import send_pictire
from asgiref.sync import sync_to_async



def get_player(pl, players):
    return [i for i in players if i.id == int(pl)][0]

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
        # actions = await sync_to_async(Actions.objects.all, thread_sensitive=True)()
        # match_info = MatchInfo(
        #     game_name=game_name,
        #     game_date=game_date,
        #     players=players,
        #     actions=actions
        # )
        halfs_players = r.keys()

        players_list = set(map(lambda x: x.split(':')[1], halfs_players))
        for pl in players_list:
            result = {}
            # player = await sync_to_async([i for i in players if i.id == int(pl)][0])
            player = [i for i in players if i.id == int(pl)][0]
            # player = await sync_to_async(get_player)(pl=pl, players=players)
            halfs = [key for key in halfs_players if key.endswith(f':{pl}')]
            result['photo'] = player.photo
            result['actions'] = {}
            for h in halfs:
                half = h.split(':')[0]
                data = r.hgetall(h)
                for  action in actions:
                    if action.name not in result['actions']:
                        result['actions'].setdefault(action.name, {})
                    value = {i: data[f'{action.slug}-{i}'] for i in self.status}
                    result['actions'][action.name][half] = value
            # ResultsJson.objects.create(
            #     player=player,
            #     value=result['actions']
            # )


            # test2.delay()

            d = accumulate_statistic(result['actions'])
            image = OurTeamImage()
            image.make_header(game_name, game_date, player.name, result['photo'])
            image.put_statistic(d)
            im = image.save_to_bytes().encode()
            final_task.delay(photo=im)





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
