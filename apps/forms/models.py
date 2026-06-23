from django.db import models
from django.contrib.auth import get_user_model
from apps.participants.models import Visit

User = get_user_model()


class FormTemplate(models.Model):
    name = models.CharField(max_length=255)
    schema_json = models.JSONField()
    version = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class FormResponse(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name="forms")
    template = models.ForeignKey(FormTemplate, on_delete=models.CASCADE)
    answers_json = models.JSONField()
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    completed_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField()

    def __str__(self):
        return f"{self.template.name} ({self.visit})"