import os

from celery import Celery
from celery.schedules import crontab

# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orchestration.settings")

# you change change the name here
app = Celery("orchestration")

# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# load tasks.py in django apps
app.autodiscover_tasks()

# Set up celery beat for scheduled strategy runs
app.conf.beat_scheduler = "django_celery_beat.schedulers.DatabaseScheduler"
app.conf.beat_schedule = {
    "check-every-minute-crontab": {
        "task": "scheduled_run_strategy",
        "schedule": crontab(),  # runs every minute
    },
}
