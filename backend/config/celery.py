import os
from celery import Celery
from celery.schedules import crontab

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create Celery app
app = Celery('config')

# Load config from Django settings with CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'cleanup-expired-users': {
        'task': 'apps.users.tasks.cleanup_expired_users',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    'send-daily-digest': {
        'task': 'apps.users.tasks.send_daily_digest',
        'schedule': crontab(hour=8, minute=0, day_of_week='1-5'),  # Weekdays 8 AM
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
