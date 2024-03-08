# from celery import shared_task
# from aiogram import Bot, Dispatcher
# from tg_bot.tgbot.config import load_config, bot, dp
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
# from asgiref.sync import async_to_sync
# import asyncio
# # from todo.celery import celery_event_loop
# from aiogram import types
#
# config = load_config()
# celery_event_loop = asyncio.new_event_loop()
#
#
#
#
# async def test1(photo):
#     asyncio.new_event_loop()
#     photo = photo.decode()
#     await bot.send_message(336112599, types.InputFile(photo))
#
#

from celery import shared_task
from todo.todo.celery1 import app
import time
#
@shared_task(name='t1',queue='q1')
def t_1():
    print('111111')
    return 'success'

@shared_task(name='t2', queue='q2')
def test_2():
    print('2222222')
    time.sleep(2)
    return 'Success'

d = t_1.delay()
# test_2.delay()

print(d)

# result = app.AsyncResult(d)
result = d.get()
print(111)
print(result)

