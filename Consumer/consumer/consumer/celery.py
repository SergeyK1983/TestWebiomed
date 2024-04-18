import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'consumer.settings')

app = Celery('consumer')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'calculate_analytic-every-3-minutes': {
        'task': 'analytics.tasks.calculate_analytic',
        'schedule': crontab(minute='0', hour='*/1'),  # каждый час
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

