from django.db import models
from apps.studies.models import Study

# Create your models here.
class Participant(models.Model):
    #the study belonging to this participant
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name="participants")
    #the id of the participant
    participant_code = models.CharField(max_length=50)
    #year of birth
    birth_year = models.IntegerField(null=True, blank=True)
    #gender
    sex = models.CharField(max_length=10,choices=[("M", "Male"), ("F", "Female"), ("O", "Other")], blank=True)
    #the baseline date of the participant
    enrolled_at = models.DateField()
    class Meta:
        #the study id and participant code together must be unique
        unique_together = ("study", "participant_code")
    
    def __str__(self):
        return f"{self.study.protocol_id} - {self.participant_code}"
    
class Visit(models.Model):
    #a participant will visit our clinic so it'll be the foreign key
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="visits")
    #the start dates at which a participant can visit
    VISIT_TYPES = [('baseline', 'Baseline'), ('month_3', 'Month 3'), ('year_1', 'Year 1')]

    visit_type = models.CharField(max_length=20, choices=VISIT_TYPES)
    #the actual date when the participant visits. For eg: if participant visits on Jan 15th then visit_type will be baseline (as its the 1st month) and visit_date will be 15/01/2026
    visit_date = models.DateField()

    class Meta:
        #a participant can visit at a single start date only. For eg: if p1 has visit_type of baseline then same p1 can't have a visit_type of month_3
        unique_together = ("participant", "visit_type")
        ordering = ["visit_date"]

    def __str__(self):
        return f"{self.participant} - {self.visit_type}"