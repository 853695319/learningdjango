import time
from celery import task


@task
def sayhello():
    print('hello...')
    for i in range(5):
        print(i)
        time.sleep(1)
    print('world...')
