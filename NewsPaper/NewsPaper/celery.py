import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'print_every_5_seconds': {
        'task': 'NewsPortal.tasks.printer',
        'schedule': 5,
        'args': (5,),
    },
    'action_every_monday_8am': {
        'task': 'NewsPortal.tasks.weekly_email_task',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
