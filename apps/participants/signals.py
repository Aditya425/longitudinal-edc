from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Participant
from .services import schedule_visits_for_participant
from .protocol import VISIT_SCHEDULE

#the receiver function
@receiver(post_save, sender=Participant)
#here instance is the participant object
def create_visits_for_new_participant(sender, instance, created, **kwargs):
    if not created:
        return
    #if a participant object is created then call the auto scheduler function. We use the VISIT_SCHEDULE list as it contains target_day and windows for baseline, month_3 and year_1
    schedule_visits_for_participant(instance, VISIT_SCHEDULE)