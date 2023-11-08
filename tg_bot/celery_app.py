from celery import Celery, shared_task
import os
# from tg_bot.tgbot.config import bot
from tgbot.config import bot
import asyncio
import environs

env = environs.Env()
password = env('RABBITMQ_PASSWORD')
user = env('RABBITMQ_USER')
app = Celery('bot', broker=f'pyamqp://{user}:{password}@rabbitmq:5672//')
# app = Celery('bot', broker='pyamqp://localhost:5672//')
celery_event_loop = asyncio.new_event_loop()

async def send_text():
    asyncio.new_event_loop()
    await bot.send_message(336112599, '=)))')



@shared_task(name='test1', queue='q1')
def test1(mes):
    celery_event_loop.run_until_complete(send_text())





