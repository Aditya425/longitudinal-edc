import os
from celery import Celery

# set config/settings.py as the default settings file for django, if not already set
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# initialize celery object. Provide project name (which is "config") as parameter to constructor
app = Celery("config")

# The settings for celery is located in config/settings.py and all of them will be a key = value. The key will have the prefix "CELERY" which is what we're saying using namespace
app.config_from_object("django.conf:settings", namespace = "CELERY")

# this command starts searching for tasks from the task queue (redis)
app.autodiscover_tasks()