from celery import Celery


app = Celery(
    'my_learning_app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
    include=['tasks']
)

app.conf.task_track_started = True