from django.contrib.auth.models import Group
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.http import HttpResponse, HttpRequest
from django.views.generic.base import TemplateView
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404

from .models import Actions, Players, Game
from .count import accumulate_statistic
from .utils.collect_data import RedisCollection, CustomRedis
from .tasks import make_and_send_image, add_result_to_db

from dataclasses import dataclass
import redis
import json

r = CustomRedis(host='172.26.0.2', port=6379, decode_responses=True)
seldom_actions = ['Обводка', 'Перехват', 'Отбор']


@dataclass
class MatchInfo:
    game: Game
    players: list
    actions: list


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
    template_name = 'statist/initial.html'

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

class InitView(GroupRequiredMixin, TemplateView):
    template_name = 'statist/initial.html'

    def get(self, request):
        player_matches = request.user.game_set.filter(finished=False, active=True)
        return self.render_to_response(context={'matches': player_matches})



class CountStatisticView(GroupRequiredMixin, TemplateView):
    template_name = 'statist/statistic.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        game = get_object_or_404(Game, pk=self.kwargs.get('game_id'))
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
                'game': game,
                'actions': actions,
                'statistic_type': 1})


    def post(self, request, *args, **kwargs):

        game_name = request.POST.get('game-name')
        game_date = request.POST.get('game-date')
        print(game_date)
        game_url = request.POST.get('game_url')
        game = Game(
            name=game_name,
            date=game_date,
            user=request.user,
            url=game_url,
        )
        game.save()
        return redirect('statistic:count_existed', game.id)





def get_player(pl, players):
    return [i for i in players if i.id == int(pl)][0]


def collect_value(key):
    half = key.split(':')[0]
    data = r.hgetall(key)
    return half, data


def approriate_view(data, action):
    status = ('success', 'fail')
    value = {i: data[f'{action.slug}-{i}'] for i in status}
    return value


def get_player_info(game_keys, player_obj: Players, match_info: MatchInfo):
    new_player = {}
    player_keys = [key for key in game_keys if f':{player_obj.id}:' in key]
    new_player['name'] = player_obj.name
    new_player['actions'] = dict()
    for key in player_keys:
        half, data = collect_value(key)
        for action in match_info.actions:

            if action.name not in new_player['actions']:
                new_player['actions'].setdefault(action.name, {})
            value = approriate_view(data, action)
            new_player['actions'][action.name][half] = value
    return new_player


class ResultStatisticView(GroupRequiredMixin, TemplateView):
    template_name = 'statistic/count.html'
    status = ('success', 'fail')

    def get(self, request, *args, **kwargs):
        game_id = self.kwargs.get('game_id')
        game = get_object_or_404(Game, pk=game_id)
        result = dict(match={'match_name': game.name, 'match_date': game.date, }, players=list())

        players = Players.objects.all()
        actions = Actions.objects.all()
        match_info = MatchInfo(
            game=game,
            players=players,
            actions=actions
        )

        game_keys = r.keys(f'{game.id}:*')
        players_id_list = [id_.split(':')[1] for id_ in game_keys]

        for player_id in players_id_list:
            player_obj = [i for i in match_info.players if i.id == int(player_id)][0]
            new_player = get_player_info(game_keys, player_obj, match_info)
            result['players'].append(new_player)

        for player in result['players']:
            add_result_to_db.delay(player, match_info.game.id)
            d = accumulate_statistic(player['actions'])
            make_and_send_image.delay(game.name, game.date, player.get('name'), d)
            r.delete(*game_keys)
            game.finished = True
            game.save()
        return JsonResponse({'status': 'hello'})


def get_any_data(request, *args):
    data = json.load(request)
    return (data.get(i) for i in args)


def initial_players(request):
    data = json.load(request)
    game_id = data.get('game_id')
    keys = (f'{game_id}:{data["player_id"]}:1', f'{game_id}:{data["player_id"]}:2')

    mapping = {action: 0 for action in data.get('actions')}
    for half, key in enumerate(keys, start=1):
        data_half = r.hgetall(key)
        if data_half:
            data_exist = True
            return JsonResponse({'status': 'exist'})
        else:
            r.hset(key, mapping=mapping)
    return JsonResponse({'status': 'ok'})


def connect_redis():
    return redis


def count_statistic(request):
    half, player_id, action, game_id = get_any_data(request, 'half', 'player_id', 'action', 'game_id')
    key = f'{game_id}:{player_id}:{half}'
    r.hincrby(key, action, 1)
    new_value = r.hget(key, action)

    return JsonResponse({'response': 'ok',
                         'value': new_value})


def get_player_data(request):

    half, player_id, game_id = get_any_data(request, 'half', 'player_id', 'game_id')
    key = f'{game_id}:{player_id}:{half}'

    res = r.hgetall(key)

    response = {
        'status': 'ok',
        'data': res
    }
    return JsonResponse(response)


def on_close(request):
    data = json.load(request)
    request.session['video_stopped'] = data.get('timing')
    return JsonResponse({'response': 'ok'})


def get_prepopulated_players(request):
    data = json.load(request)
    game_id = data.get('game_id', None)
    d = set(map(lambda x: x.split(':')[1], r.keys(f'{game_id}:*')))
    return JsonResponse({'status': 'ok',
                         'players': [*d]})