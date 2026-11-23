from celery import Celery
from celery.schedules import crontab


app = Celery(
    'my_learning_app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
    include=['tasks']
)

app.conf.task_track_started = True
app.conf.beat_schedule = {
    'cleanup-every-30-seconds': {
        'task': 'tasks.cleanup_temp_files',
        'schedule': 30.0,
    },
    'daily-report-at-3am': {
        'task': 'tasks.generate_daily_report',
        'schedule': crontab(hour=3, minute=0),
    },
    'ping-service-every-minute': {
        'task': 'tasks.ping_external_service',
        'schedule': crontab(minute='*/1'),
        'args': ('https://example.com',),
    },
}
