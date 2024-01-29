from dataclasses import dataclass
import redis
import json
from django import forms

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse, HttpRequest
from django.urls import reverse
from django.views.generic import FormView, ListView, DetailView
from django.views.generic.base import TemplateView
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404, render
from django.db.models import Q

from .forms import InitForm
from .models import Actions, Players, Game, Type, Parts
from .count import accumulate_statistic
from .statistic_to_image import OurTeamImage
from .tasks import make_and_send_image, add_result_to_db
from django.template import loader
from django.http import HttpResponseForbidden


r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
# r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD, decode_responses=True)
seldom_actions = ['Обводка', 'Перехват', 'Отбор']


@dataclass
class MatchInfo:
    game: Game
    players: list
    actions: list



class InitView(PermissionRequiredMixin, FormView):
    # form_class = InitForm
    template_name = 'statist/initial.html'
    permission_required = 'statist.can_add_new_game'

    def get_types(self):
        return Type.objects.values_list('id', 'name').filter(Q(user=self.request.user.id) | Q(user=None))

    def get_form(self, form_class=InitForm):
        form = InitForm()
        form.fields['test_name'] = forms.ChoiceField(choices=self.get_types())
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['types'] = Type.objects.filter(Q(user=self.request.user.id) | Q(user=None))
        context['matches'] = self.request.user.game_set.filter(finished=False, active=True)
        return context

    def handle_no_permission(self):
        return redirect(f'{settings.LOGIN_URL}?next={self.request.path}')


    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = InitForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            tt = cd['test_name']
            game = Game(
                name=cd['name'],
                date=cd['date'],
                user=request.user,
                url=cd['url'],
                type_id=cd['test_name']
            )
            game.save()
            # return redirect('statistic:count_existed', game.id)
            return redirect(game, game.id)
        context = self.get_context_data()
        return render(request, 'statist/initial.html', context=context)
    # можно ли заменить на super().post()



class CountStatisticView(PermissionRequiredMixin, TemplateView):
    template_name = 'statist/statistic.html'
    permission_required = 'statist.can_add_new_game'

    def get(self, request: HttpRequest, *args, **kwargs):
        print(self.kwargs)
        print(request.POST)
        # game_type = int(self.kwargs.get('type-select'))
        # halfs = get_object_or_404(Type, id=game_type).halfs
        # print(f'{halfs=}')
        game_id = self.kwargs.get('game_id')
        d = get_object_or_404(Game, id=game_id).type.id
        print(d)
        # game = get_object_or_404(Game, pk=self.kwargs.get('game_id'))
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
                'game_id': game_id,
                'actions': actions,
                'statistic_type': 1})



def get_player(pl, players):
    return [i for i in players if i.id == int(pl)][0]


def collect_value(key):
    half = key.split(':')[2]
    data = r.hgetall(key)
    return half, data


def approriate_view(data, action):

    value_fail = int(data[f'{action.slug}-{"fail"}'])
    value_success = int(data[f'{action.slug}-{"success"}'])
    total = value_fail + value_success
    try:
        value_percent = value_success / total * 100
    except ZeroDivisionError:
        value_percent = 0
    # value['total'] = sum(int(value[i]) for i in status)

    return value_success, value_fail, value_percent


def get_player_info(game_keys, player_obj: Players, match_info: MatchInfo):
    new_player = {}
    itog_dict = {}
    previous_half = 0
    player_keys = [key for key in game_keys if f':{player_obj.id}:' in key]
    first = True if len(player_keys) > 1 else False
    for key in player_keys:
        actions = {}
        half_data = {}
        half, data = collect_value(key)
        for action in match_info.actions:
            # if action.name not in actions:

            value_success, value_fail, value_percent = approriate_view(data, action)
            actions[action.name] = {'success': value_success, 'fail': value_fail, 'percent': value_percent}

            try:
                prev_value_dict = new_player[previous_half][player_obj.name][action.name]
                prev_value_success = prev_value_dict['success'] + value_success
                prev_value_fail = prev_value_dict['fail'] + value_fail
                total = prev_value_success + prev_value_fail
                try:
                    itog_percent = prev_value_success / total * 100
                except ZeroDivisionError:
                    itog_percent = 0
                itog_dict[action.name] = {'success': prev_value_success, 'fail': prev_value_fail, 'percent': itog_percent}
            except KeyError:
                itog_dict[action.name] = {'success': value_success, 'fail': value_fail, 'percent': value_percent}

        previous_half = half
        # для добавления значений в бд сделать чтобы можно было пробегаться по таймам (из бд) и сохранять для каждого игрока.

        half_data[player_obj.name] = actions
        new_player[half] = half_data
    new_player['itog'] = {player_obj.name: itog_dict}

    return new_player


from pprint import pprint

class ResultStatisticView(PermissionRequiredMixin, TemplateView):
    permission_required = 'statist.can_add_new_game'
    template_name = 'statist/success.html'
    status = ('success', 'fail')

    def get(self, request, *args, **kwargs):
        game_id = self.kwargs.get('game_id')
        game = get_object_or_404(Game, pk=game_id)
        res = {}
        # add half to Game model to store amount of halfs and put it to match info
        result = dict(match={'match_name': game.name, 'match_date': game.date, }, data=dict())
        players = Players.objects.all() # ?
        actions = Actions.objects.all() # ?
        match_info = MatchInfo(
            game=game,
            players=players,
            actions=actions
        )

        game_keys = r.keys(f'{game.id}:*')
        players_id_list = set([id_.split(':')[1] for id_ in game_keys])
        halfs_list = set([id_.split(':')[2] for id_ in game_keys]) # halfs get from db models
        halfs_list = list(halfs_list)
        halfs = {}
        for player_id in players_id_list:
            player_obj = [i for i in match_info.players if i.id == int(player_id)][0]
            new_player = get_player_info(game_keys, player_obj, match_info)
            print(f'{new_player=}')
            # res |= new_player
            for h in halfs_list + ['itog']:
                if h not in res:
                    res[h] = {}
                res[h].update(new_player[h])
        print(res)





        # for half in halfs_list:
        #     half_data = {}
        #
        #     for player_id in players_id_list:
        #         player_obj = [i for i in match_info.players if i.id == int(player_id)][0]
        #         new_player = get_player_info(game_keys, player_obj, match_info)
        #         half_data.update(new_player)
        #
        #     result['data'].update({half: half_data})




        # for player_id in players_id_list:
        #     player_obj = [i for i in match_info.players if i.id == int(player_id)][0]
        #     new_player = get_player_info(game_keys, player_obj, match_info)
        #     result['players'].update(new_player)
        # print(result)

        # for player in result['players']:
        #
        #     add_result_to_db.delay(player, match_info.game.id)
            # d = accumulate_statistic(player['actions'])
            # players_result_actions[player['name']] = d
            # make_and_send_image.delay(game.name, game.date, player.get('name'), d)
        r.delete(*game_keys)
        game.finished = True
        game.save()
        return self.render_to_response(context={
            'match_name': result['match']['match_name'],
            'match_date': result['match']['match_date'],
            'players': result['players'],
            'actions': actions
        })



def get_any_data(request, *args):
    data = json.load(request)
    return (data.get(i) for i in args)



# Сделать один запрос со всеми добавленными игроками, а не делать много запросов с одним игроком.
def initial_players(request):
    data = json.load(request)
    game_id = data.get('game_id')
    keys = (f'{game_id}:{data["player_id"]}:1', f'{game_id}:{data["player_id"]}:2')

    mapping = {action: 0 for action in data.get('actions')}
    for half, key in enumerate(keys, start=1):
        data_half = r.hgetall(key)
        if data_half:
            return JsonResponse({'status': 'exist'})
        else:
            r.hset(key, mapping=mapping)
    return JsonResponse({'status': 'ok'})


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


def delete_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    game.active = False


def error_forbidden_view(request, exception):
    content = loader.render_to_string('errors/error403.html', {}, request)
    return HttpResponseForbidden(content=content)


#=========================================================
from django.forms.models import BaseInlineFormSet
from django.forms import inlineformset_factory

class BaseChildrenFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)

        form.nested = PartsFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='parts-%s-%s' % (
                form.prefix,
                PartsFormset.get_default_prefix()),
        )

    def is_valid(self):
        result = super().is_valid()
        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()
        return result

    def save(self, commit=True):
        result = super().save(commit=commit)
        for form in self.forms:
            print(form.nested.forms[0])
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    d = form.nested.save(commit=commit)
                    print(d)


        return result



TypeFormset = inlineformset_factory(Type, Parts, fields=['name',], formset=BaseChildrenFormset, extra=0, can_delete=False)
PartsFormset = inlineformset_factory(Parts, Actions, fields=['name'], extra=0, can_delete=False)



class TypesManageView(ListView):
    model = Type

    def get_queryset(self):
        return Type.objects.filter(user=self.request.user)


class TypesDetailView(TemplateView):
    template_name = 'statist/create_type.html'

    def get(self, request, *args, **kwargs):
        current_type = get_object_or_404(Type, pk=self.kwargs['id'])
        formset = TypeFormset(instance=current_type)

        context = self.get_context_data(**kwargs)
        context['formset'] = formset
        context['current_type'] = current_type
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        current_type = get_object_or_404(Type, pk=self.kwargs['id'])
        form1 = TypeFormset(request.POST, instance=current_type)
        # print(form1.is_valid())
        if form1.is_valid():
            print('valid')
            z = form1.save()
        return self.render_to_response({})
