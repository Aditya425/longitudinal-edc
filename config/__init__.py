#import the celery object which is created in celery.py. Rename it to celery_app for clarity
from .celery import app as celery_app

#include it in __all__ so that celery can access this object
__all__ = ("celery_app")