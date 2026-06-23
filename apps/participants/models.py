from django.db import models
from django.contrib.auth import get_user_model
from apps.studies.models import Study

User = get_user_model()

class Participant(models.Model):
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name="participants")
    participant_code = models.CharField(max_length=50)
    birth_year = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=10, choices=[("M", "Male"), ("F", "Female"), ("O", "Other")], blank=True)
    enrolled_at = models.DateField()

    class Meta:
        unique_together = ("study", "participant_code")

    def __str__(self):
        return f"{self.study.protocol_id} - {self.participant_code}"

class Visit(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="visits")
    VISIT_TYPES = [('baseline', 'Baseline'), ('month_3', 'Month 3'), ('year_1', 'Year 1')]
    visit_code = models.CharField(max_length=20, choices=VISIT_TYPES)
    actual_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()
    window_start = models.DateField(null=True)
    window_end = models.DateField(null=True)
    deviation_reason = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('missed', 'Missed')],
        default="scheduled"
    )

    class Meta:
        unique_together = ("participant", "visit_code")
        ordering = ["due_date"]

    def __str__(self):
        return f"{self.participant} - {self.visit_code}"

class VisitDeviation(models.Model):
    visit = models.OneToOneField(Visit, on_delete=models.CASCADE, related_name="deviation")
    reason = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deviation: {self.visit}"