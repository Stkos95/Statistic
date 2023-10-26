from django.contrib.auth.models import Group
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.conf import settings

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


class CountStatisticView(GroupRequiredMixin, TemplateView):
    template_name = 'statist/statistic.html'

    def get(self, request, *args, **kwargs):
        new_redis_index = request.session.get(settings.REDIS_DB_ID, None)
        if not new_redis_index:
            new_redis_index = r.get_new_db_index()
            request.session[settings.REDIS_DB_ID] = new_redis_index
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


class InitView(GroupRequiredMixin, TemplateView):
    pass


def get_player(pl, players):
    return [i for i in players if i.id == int(pl)][0]


def collect_value(r: RedisCollection, key):
    half = key.split(':')[0]
    data = r.get_hash_data_for_player(key)
    return half, data


def approriate_view(data, action):
    status = ('success', 'fail')
    value = {i: data[f'{action.slug}-{i}'] for i in status}
    return value


def get_player_info(r: RedisCollection, player_obj: Players, match_info: MatchInfo):
    new_player = {}

    keys = r.get_keys_for_player(player_obj.id)
    new_player['name'] = player_obj.name
    new_player['actions'] = dict()
    for key in keys:
        half, data = collect_value(r, key)
        for action in match_info.actions:

            if action.name not in new_player['actions']:
                new_player['actions'].setdefault(action.name, {})
            value = approriate_view(data, action)
            new_player['actions'][action.name][half] = value
    return new_player


class ResultStatisticView(GroupRequiredMixin, TemplateView):
    template_name = 'statistic/count.html'
    status = ('success', 'fail')

    def post(self, request, *args, **kwargs):
        game_name = request.POST.get('game-name')
        game_date = request.POST.get('game-date')
        game = Game(name=game_name,
                    slug=f'{game_name}_slug',
                    date=game_date)
        game.save()
        result = dict(match={'match_name': game_name, 'match_date': game_date, }, players=list())

        players = Players.objects.all()
        actions = Actions.objects.all()
        match_info = MatchInfo(
            game=game,
            players=players,
            actions=actions
        )

        rr = RedisCollection(host=settings.REDIS_HOST,
                             port=settings.REDIS_PORT,
                             decode_responses=True,
                             db=request.session.get(settings.REDIS_DB_ID))

        for player_id in rr.get_player_ids_list():
            player_obj = [i for i in match_info.players if i.id == int(player_id)][0]
            new_player = get_player_info(rr, player_obj, match_info)
            result['players'].append(new_player)
        for player in result['players']:
            print(match_info.game.id)
            add_result_to_db.delay(player, match_info.game.id)
            d = accumulate_statistic(player['actions'])
            make_and_send_image.delay(game_name, game_date, player.get('name'), d)

            rr.flushdb()
            print(request.session[settings.REDIS_DB_ID])
            del request.session[settings.REDIS_DB_ID]
        return JsonResponse({'status': 'hello'})


def get_any_data(request, *args):
    data = json.load(request)
    return (data.get(i) for i in args)


def initial_players(request):
    rr = CustomRedis(host=settings.REDIS_HOST,
                     port=settings.REDIS_PORT,
                     decode_responses=True,
                     db=request.session.get(settings.REDIS_DB_ID))
    data = json.load(request)

    keys = (f'1:{data["player_id"]}', f'2:{data["player_id"]}')
    mapping = {action: 0 for action in data.get('actions')}
    result = {}
    for half, key in enumerate(keys, start=1):
        data_half = rr.hgetall(key)
        if data_half:
            data_exist = True
            return JsonResponse({'status': 'exist'})
            # break
        else:
            rr.hset(key, mapping=mapping)
    # if data_exist:
    #     return JsonResponse({'status': 'exist'})

    return JsonResponse({'status': 'ok'})


def connect_redis():
    return redis


def count_statistic(request):
    rr = CustomRedis(host=settings.REDIS_HOST,
                     port=settings.REDIS_PORT,
                     decode_responses=True,
                     db=request.session.get(settings.REDIS_DB_ID))
    half, player_id, action = get_any_data(request, 'half', 'player_id', 'action')
    key = f'{half}:{player_id}'
    rr.hincrby(key, action, 1)
    new_value = rr.hget(key, action)

    return JsonResponse({'response': 'ok',
                         'value': new_value})


def get_player_data(request):
    # rr = CustomRedis(host='172.26.0.2', port=6379, decode_responses=True, db=request.session.get(settings.REDIS_DB_ID))
    rr = CustomRedis(host=settings.REDIS_HOST,
                     port=settings.REDIS_PORT,
                     decode_responses=True,
                     db=request.session.get(settings.REDIS_DB_ID))
    half, player_id = get_any_data(request, 'half', 'player_id')
    key = f'{half}:{player_id}'

    res = rr.hgetall(key)

    response = {
        'status': 'ok',
        'data': res
    }
    return JsonResponse(response)


def celery_test(request):
    add.apply_async()
    return JsonResponse({'response': 'ok'})
