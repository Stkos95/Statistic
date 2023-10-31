from django.contrib.auth.models import Group
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.http import HttpResponse
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
        player_matches = request.user.game_set.filter(finished=False)
        return self.render_to_response(context={'matches': player_matches})



class CountStatisticView(GroupRequiredMixin, TemplateView):
    template_name = 'statist/statistic.html'

    def get(self, request, *args, **kwargs):
        game = get_object_or_404(Game, pk=self.kwargs.get('game_id'))
        # if not game.bd_index:
        #     raise HttpException
        request.session[settings.REDIS_DB_ID] = game.bd_index
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
        print(f'{self.__class__.__name__}-{r.indexes=}')
        return self.render_to_response(
            context={
                'actions_by_category': action_by_category,
                'players': players,
                'game': game,
                'actions': actions,
                'statistic_type': 1})


    def post(self, request, *args, **kwargs):


        game_name = request.POST.get('game-name')
        game_date = request.POST.get('game_date')
        game_url = request.POST.get('game_url')
        # new_redis_index = request.session.get(settings.REDIS_DB_ID, None)
        new_redis_index = r.get_new_db_index()
        game = Game(
            name=game_name,
            date=game_date,
            user=request.user,
            url=game_url,
            bd_index=new_redis_index
        )
        game.save()
        r.indexes.append(new_redis_index)
        print(f'{self.__class__.__name__}-{r.indexes=}')
        request.session[settings.REDIS_DB_ID] = new_redis_index
        return redirect('statistic:count_existed', game.id)


        # if not new_redis_index:
        #     new_redis_index = r.get_new_db_index()
        #     request.session[settings.REDIS_DB_ID] = new_redis_index






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

        rr = RedisCollection(host=settings.REDIS_HOST,
                             port=settings.REDIS_PORT,
                             decode_responses=True,
                             db=request.session.get(settings.REDIS_DB_ID))

        players_ids_list = r.keys



        # for player_id in rr.get_player_ids_list():
        #     player_obj = [i for i in match_info.players if i.id == int(player_id)][0]
        #     new_player = get_player_info(rr, player_obj, match_info)
        #     result['players'].append(new_player)
        # for player in result['players']:
        #     add_result_to_db.delay(player, match_info.game.id)
        #     d = accumulate_statistic(player['actions'])
        #     make_and_send_image.delay(game.name, game.date, player.get('name'), d)
        #     print(f'{self.__class__.__name__}-{r.indexes=}')
        #     rr.flushdb()
        #     r.indexes.remove(game.bd_index)
        #     game.finished = True
        #     # game.bd_index = None
        #     game.save()
        #     print(f'after remove: {self.__class__.__name__}-{r.indexes=}')
        #     del request.session[settings.REDIS_DB_ID]
        # return JsonResponse({'status': 'hello'})


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
    print(request.session.get(settings.REDIS_DB_ID))
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


def on_close(request):
    data = json.load(request)
    request.session['video_stopped'] = data.get('timing')
    return JsonResponse({'response': 'ok'})


def get_prepopulated_players(request):
    data = json.load(request)
    db_index = data.get('db_index', None)
    rr = CustomRedis(host=settings.REDIS_HOST,
                     port=settings.REDIS_PORT,
                     decode_responses=True,
                     db=int(db_index))
    players = rr.keys()
    d = set(map(lambda x: x.split(':')[1], players))







    return JsonResponse({'status': 'ok',
                         'players': [*d]})