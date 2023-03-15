import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fannote.settings')
 
app = Celery('fannote')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'create_weekly_news_mail': {
        'task': 'users.tasks.news_mail',
        # 'schedule': crontab(minute='*/5'),
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
