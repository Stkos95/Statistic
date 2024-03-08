from dataclasses import dataclass
import redis
import json
from django import forms

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.urls import reverse
from django.views.generic import FormView, ListView, DetailView, CreateView
from django.views.generic.base import TemplateView
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404, render
from django.db.models import Q

from .forms import InitForm

from django.forms.models import BaseInlineFormSet
from django.forms import inlineformset_factory, HiddenInput, ValidationError
# from .forms import PartsForm, CreateTypeGame
from .key_schema import KeySchema
from .models import Actions, Players, Game, Type, Parts, RawResults, Teams
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
    is_new: bool = False



class InitView(PermissionRequiredMixin, FormView):
    # form_class = InitForm
    template_name = 'statist/initial.html'
    permission_required = 'statist.can_add_new_game'

    def get_types(self):
        return Type.objects.values_list('id', 'name').filter(Q(user=self.request.user.id) | Q(user=None))

    def get_form(self, form_class=InitForm):
        form = InitForm(request=self.request)
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
        form = InitForm(data=request.POST, request=request)
        if form.is_valid():
            cd = form.cleaned_data
            tt = cd['test_name']
            game = Game(
                name=cd['name'],
                date=cd['date'],
                user=request.user,
                url=cd['url'],
                type_id=cd['test_name'],
                team_id=cd['teams']
            )
            game.save()
            return redirect(game, game.id)
        context = self.get_context_data()
        return render(request, 'statist/initial.html', context=context)
    # можно ли заменить на super().post()



class CountStatisticView(PermissionRequiredMixin, TemplateView):
    template_name = 'statist/statistic.html'
    permission_required = 'statist.can_add_new_game'

    def get(self, request: HttpRequest, *args, **kwargs):
        game_id = self.kwargs.get('game_id')
        game = get_object_or_404(Game, pk=self.kwargs.get('game_id'))
        type_game = game.type
        halfs = [i + 1 for i in range(type_game.halfs)]
        players = game.team.players_set.all()
        action_parts = type_game.parts.all()
        actions = type_game.actions.all()
        keys_current_game = r.keys(f'{game_id}:*')
        if keys_current_game:
            prepopulated_players = map(lambda x: x.split(':')[1], keys_current_game)
            print(prepopulated_players)

        return self.render_to_response(
            context={
                'action_parts': action_parts,
                'players': players,
                'game_id': game_id,
                'game': game,
                'actions': actions,
                'statistic_type': type_game,
                'halfs': halfs})



def get_player(pl, players):
    return [i for i in players if i.id == int(pl)][0]


def collect_value(key):
    data = r.hgetall(key)
    return data


def approriate_view(data, action):
    value_fail = int(data[f'{action.slug}-{"fail"}'])
    value_success = int(data[f'{action.slug}-{"success"}'])
    total = value_fail + value_success
    try:
        value_percent = value_success / total * 100
    except ZeroDivisionError:
        value_percent = 0
    return value_success, value_fail, value_percent


def get_player_info(player_keys: list, player_obj: Players, match_info: MatchInfo):
    new_player = {}
    itog_dict = {}
    previous_half = 0
    for key in player_keys:
        actions = {}
        half = key.split(':')[2]
        if match_info.is_new:
            data = collect_value(key)
            add_to_db_task(player=player_obj, game=match_info.game, half=half, value=data)
        else:
            data = RawResults.objects.get(game=match_info.game, player=player_obj, half=half).value_js
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
        new_player[half] = actions
    new_player['itog'] = itog_dict

    return new_player


from pprint import pprint

def process_raw_result_data(player_obj, match_info):


    if match_info.is_new:
        add_to_db_task(player_obj, match_info)


def add_to_db_task(player, game, half, value):
    RawResults.objects.create(
        player=player,
        game=game,
        half=half,
        value_js=value
    )


class ResultStatisticView(PermissionRequiredMixin, TemplateView):
    permission_required = 'statist.can_add_new_game'
    template_name = 'statist/success.html'



    def post(self, request, *args, **kwargs):
        print(request.POST)
        game = get_object_or_404(Game, pk=self.kwargs.get('game_id'))
        res = {}
        players = game.team.players_set.all() # ?
        print(players)
        match_info = MatchInfo(
            game=game,
            players=players,
            actions=game.type.actions.all(),
            is_new=True
        )
        game_keys = r.keys(f'{game.id}:*')

        players_id_list = request.POST.getlist('players[]')
        halfs_list = [i + 1 for i in range(game.type.halfs)]

        for player_id in players_id_list:
            player_keys = [k for k in game_keys if f':{player_id}:' in k]
            player_obj = [i for i in players if i.id == int(player_id)][0]
            new_player_data = get_player_info(player_keys, player_obj, match_info)

            for h in halfs_list + ['itog']:
                if h not in res:
                    res[h] = {}
                res[h].update({player_obj.name: new_player_data[str(h)]})


        # for player in result['players']:
        #
        #     add_result_to_db.delay(player, match_info.game.id)
        #     d = accumulate_statistic(player['actions'])
        #     players_result_actions[player['name']] = d
        #     make_and_send_image.delay(game.name, game.date, player.get('name'), d)
        # r.delete(*game_keys)

        game.finished = True
        game.save()
        return self.render_to_response(context={
            'game': game,
            'players': players,
            'result': res,
            'is_new': True

        })

    def get(self, request, *args, **kwargs):
        game_id = self.kwargs.get('game_id', None)
        player_id = self.kwargs.get('player_id', None)
        game = get_object_or_404(Game, pk=game_id)
        results = game.results.all().order_by('player')
        halfs_list = list(game.results.values_list('half', flat=True).distinct())

        players = Players.objects.all()  # ??????????????????????????????

        match_info = MatchInfo(
            game=game,
            players=players,
            actions=game.type.actions.all()
        )

        if player_id:
            results = results.filter(player_id=player_id)
        res = {}
        for player_id in results.values_list('player_id', flat=True).distinct():
            player_data = results.filter(player_id=player_id)
            player_keys = [KeySchema().hash_match_player_half(game_id, player_id, half)
                    for half in halfs_list]

            new_player_data = get_player_info(player_keys, player_data.first().player, match_info)

            for h in halfs_list + ['itog']:
                if h not in res:
                    res[h] = {}
                res[h].update({player_data.first().player: new_player_data[str(h)]})

        return self.render_to_response(context={
            'game': game,
            'players': players,
            'actions': game.type.actions.all(),
            'result': res

        })




#============================ views for JS ==========================================
def get_any_data(request, *args):
    data = json.load(request)
    return (data.get(i) for i in args)



# Сделать один запрос со всеми добавленными игроками, а не делать много запросов с одним игроком.
def initial_players(request):
    data = json.load(request)
    game_id = data.get('game_id')
    game_type = Game.objects.get(pk=game_id).type
    actions = game_type.actions.all() # Возможно сделать, чтобы получать список действий из бд, а не из запроса.
    keys = [KeySchema().hash_match_player_half(game_id, data['player_id'], half) for half in range(1, game_type.halfs + 1)]

    mapping = {action: 0 for action in data.get('actions')}
    # mapping = {action: 0 for action in data.get('actions')}
    for half, key in enumerate(keys, start=1):
        data_half = r.hgetall(key)
        if data_half:
            return JsonResponse({'status': 'exist'})
        else:
            r.hset(key, mapping=mapping)
    return JsonResponse({'status': 'ok'})


def count_statistic(request):

    data = json.loads(request.body)
    half, player_id, action, game_id = get_any_data(request, 'half', 'player_id', 'action', 'game_id')

    key = KeySchema().hash_match_player_half(game_id, player_id, half)
    if 'value' in data.keys():
        new_value = data.get('value')
        r.hset(key, action, new_value)
    else:
        new_value = r.hincrby(key, action, 1)
    return JsonResponse({'response': 'ok',
                         'value': new_value})


def get_player_data(request):
    half, player_id, game_id = get_any_data(request, 'half', 'player_id', 'game_id')
    key = KeySchema().hash_match_player_half(game_id, player_id, half)
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
    return JsonResponse({'status': 'Ok',
                         'players': [*d]})


def delete_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    game.active = False


def error_forbidden_view(request, exception):
    content = loader.render_to_string('errors/error403.html', {}, request)
    return HttpResponseForbidden(content=content)


#========================================================= manage game types (create) =======================
# class BaseTypeFormset(BaseInlineFormSet):
#     ordering_widget = HiddenInput
#
#     def add_fields(self, form, index):
#         super().add_fields(form, index)
#
#         form.nested = PartsFormset(
#             instance=form.instance,
#             data=form.data if form.is_bound else None,
#             files=form.files if form.is_bound else None,
#             prefix='parts-%s-%s' % (
#                 form.prefix,
#                 PartsFormset.get_default_prefix()),
#         )
#
#     def clean(self):
#         for form in self.forms:
#
#             for nested_form in form.nested:
#
#                 if nested_form.is_valid():
#                     # nested_form.non_field_errors()
#                     # nested_form.add_error()
#                     name = nested_form.cleaned_data.get('name', None)
#                     if not name:
#
#                         raise ValidationError("Заполните или удалите пустые поля 'Действие'.")
#
#
#
#     def save(self, commit=True):
#         r = []
#         result = super().save(commit=commit)
#         for form in self.forms:
#             if hasattr(form, 'nested'):
#                 if not self._should_delete_form(form):
#                     zz =form.nested.save(commit=False)
#                     r.extend(zz)
#         return r
#
# class BasePartFormset(BaseInlineFormSet):
#     ordering_widget = HiddenInput
#     deletion_widget = HiddenInput
#
# TypeFormset = inlineformset_factory(Type, Parts, fields=['name',], formset=BaseTypeFormset, extra=0, can_delete=False, can_order=True)
# PartsFormset = inlineformset_factory(Parts, Actions, fields=['name'], min_num=1, formset=BasePartFormset, extra=0, can_delete=True, can_order=True)
#
#
#
# class TypesManageView(ListView):
#     model = Type
#
#     def get_queryset(self):
#         return Type.objects.filter(user=self.request.user)
#
#
#
#
# class TypesDetailView(TemplateView):
#     template_name = 'statist/create_type.html'
#
#     def get(self, request, *args, **kwargs):
#         current_type = None
#         form_create = False
#         if 'id' in self.kwargs:
#             current_type = get_object_or_404(Type, pk=self.kwargs['id'])
#         else:
#                 form_create = CreateTypeGame(prefix='type') # ОСТАНОВИЛСЯ тут, дальше, в случае создания типа, нужно создать тип, а затем добавлять в бд разделы.
#         formset = TypeFormset(instance=current_type)
#
#         context = dict()
#         context['form_create'] = form_create
#         context['formset'] = formset
#         context['current_type'] = current_type
#         return self.render_to_response(context)
#
#     def post(self, request, *args, **kwargs):
#         # print(request.POST)
#         current_type = None
#         form_create = CreateTypeGame(request.POST, prefix='type')
#         if form_create.is_valid():
#             current_type = form_create.save(commit=False)
#             current_type.user_id = request.user.id
#             current_type.save()
#
#         if not current_type:
#             current_type = get_object_or_404(Type, pk=self.kwargs['id'])
#
#
#         form1 = TypeFormset(request.POST, instance=current_type)
#         if form1.is_valid():
#             parts = form1.save()
#             for action in parts:
#                 action.type = current_type
#                 action.save()
#
#         else:
#             context = self.get_context_data(**kwargs)
#             context['formset'] = form1
#             context['current_type'] = current_type
#         return self.render_to_response({})
#
#
# def test_order(request):
#     print('Пришло!!!')
#     JsonResponse({'status': 'ok',})




#===================================================

