import django
import os
import asyncio
import random
import time
from multiprocessing import Process, Value, Queue
from threading import Thread

from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Site.settings')
django.setup()


from Users.models import *
from SolveGia.models import *
from SolveGia.views import get_task_closets_to_difficulty


User = CustomUser
infa = Category.objects.get(name='Informatika')


def get_27_tasks(difficulty, category):
    tasks = []
    for i in range(1, 26):
        tasks.append(get_task_closets_to_difficulty(i, difficulty, category))
    return tasks

# print(get_27_tasks_MP(100, infa))
print('Started')
st = time.time()
for i in range(100):
    tasks = get_27_tasks(0, infa)
print(f'Finished in {time.time() - st}')