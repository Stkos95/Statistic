from celery import shared_task
from tg_bot.tgbot.config import bot
from .models import Players, Actions, Game, Results
from django.shortcuts import get_object_or_404
from .statistic_to_image import OurTeamImage
import asyncio
from aiogram import types

#
celery_event_loop = asyncio.new_event_loop()
#
@shared_task(name='add_result_to_db')
def add_result_to_db(player, game_id):
    player_obj = get_object_or_404(Players, name=player.get('name'))
    actions = Actions.objects.all()
    game = get_object_or_404(Game, id=game_id)

    for action in actions:
        for half, value in player['actions'][action.name].items():
            for status in value.keys():
                try:
                    Results.objects.create(
                        player=player_obj,
                        game=game,
                        half=half,
                        action=action,
                        status=status,
                        value=value[status],
                    )
                except Exception as e:
                    print(e)
    return 'Success'

async def send_photo(image):
    asyncio.new_event_loop()
    image.seek(0)
    await bot.send_photo(336112599, types.BufferedInputFile(image.getvalue(), filename='statistic.jpeg'))

#
#
@shared_task(name='make_and_send_image')
def make_and_send_image(game_name, game_date, player_name, data):
    player = get_object_or_404(Players, name=player_name)
    photo = player.photo
    image = OurTeamImage()
    image.make_header(game_name, game_date, player_name, photo)
    image.put_statistic(data)
    bytesio_image = image.save_to_bytes()
    celery_event_loop.run_until_complete(send_photo(bytesio_image))


#

#
# @shared_task(name='t1',queue='q1')
# def test_1():
#     print('111111')
#     time.sleep(2)
#
# @shared_task(name='t2', queue='q2')
# def test_2():
#     print('2222222')
#     time.sleep(2)

# test_1.delay()
# test_2.delay()