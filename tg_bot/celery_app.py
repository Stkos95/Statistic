from celery import Celery, shared_task
import os
# from tg_bot.tgbot.config import bot
from tgbot.config import bot
import asyncio
import environs
from aiogram import types

env = environs.Env()
password = env('RABBITMQ_PASSWORD')
user = env('RABBITMQ_USER')
app = Celery('bot', broker=f'pyamqp://{user}:{password}@rabbitmq:5672//')
# app = Celery('bot', broker='pyamqp://localhost:5672//')
celery_event_loop = asyncio.new_event_loop()


async def send_photo(photo):
    asyncio.new_event_loop()
    photo = photo.decode()
    await bot.send_message(336112599, types.InputFile(photo))


@shared_task(name='photo', queue='bot')
def send_photo_wrapper(mes):
    celery_event_loop.run_until_complete(send_photo(mes))





