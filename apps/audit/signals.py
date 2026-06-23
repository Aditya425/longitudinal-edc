from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.participants.models import Participant, Visit
from apps.studies.models import Study
from apps.forms.models import FormResponse
from .services import log_action


@receiver(post_save, sender=Study)
def audit_study_save(sender, instance, created, **kwargs):
    action = "CREATE" if created else "UPDATE"
    log_action(None, action, "Study", instance.pk, {"name": instance.name})


@receiver(post_delete, sender=Study)
def audit_study_delete(sender, instance, **kwargs):
    log_action(None, "DELETE", "Study", instance.pk, {"name": instance.name})


@receiver(post_save, sender=Participant)
def audit_participant_save(sender, instance, created, **kwargs):
    action = "CREATE" if created else "UPDATE"
    log_action(None, action, "Participant", instance.pk, {
        "participant_code": instance.participant_code,
        "study_id": instance.study_id,
    })


@receiver(post_delete, sender=Participant)
def audit_participant_delete(sender, instance, **kwargs):
    log_action(None, "DELETE", "Participant", instance.pk, {
        "participant_code": instance.participant_code,
    })


@receiver(post_save, sender=Visit)
def audit_visit_save(sender, instance, created, **kwargs):
    action = "CREATE" if created else "UPDATE"
    log_action(None, action, "Visit", instance.pk, {
        "participant_id": instance.participant_id,
        "status": instance.status,
    })


@receiver(post_save, sender=FormResponse)
def audit_form_response_save(sender, instance, created, **kwargs):
    action = "SUBMIT_FORM" if created else "UPDATE"
    log_action(None, action, "FormResponse", instance.pk, {
        "visit_id": instance.visit_id,
        "template_name": instance.template.name,
    })
