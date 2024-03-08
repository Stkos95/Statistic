from celery import Celery, shared_task
import os
from asgiref.sync import async_to_sync
import asyncio



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')

app = Celery('todo', result_backend = 'rpc://')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()



# task_routes = {'feed.tasks.import_feed': {'queue': 'feeds'}}
