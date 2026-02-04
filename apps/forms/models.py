from django.db import models
from apps.participants.models import Visit

# Create your models here.
class ClinicalForm(models.Model):
    #the visit for which this form is made for
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name="forms")
    form_name = models.CharField(max_length=100)
    #the form responses will be in the form of json so we use a JSONField() which will serialize the json automatically
    data = models.JSONField()
    #the form created date
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.form_name} ({self.visit})"