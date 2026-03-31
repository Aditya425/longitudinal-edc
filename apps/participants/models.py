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

    visit_code = models.CharField(max_length=20, choices=VISIT_TYPES)
    #the actual date when the participant visits. For eg: if participant visits on Jan 15th then visit_code will be baseline (as its the 1st month) and actual_date will be 15/01/2026
    #if actual_date is null then it means the participant hasn't visited yet
    actual_date = models.DateField(null=True, blank=True)
    #the ideal date when the participant should visit. For eg: if we consider baseline as Jan 1 then due_date will be Jan 1 (the actual date which participant visited is recorded in actual_date). Also when we calculate dates after baseline then it is: due_date = baseline + visit_type. Eg: if baseline is on Jan 1 and we want to calculate the due_date for the participant for month 3 then we do: Jan 1 + month_3 = Jan 1 + 90 = April 1 i.e 01/04/2026
    due_date = models.DateField()
    #window_before and window_after. This is the date not days
    window_start = models.DateField(null=True)
    window_end = models.DateField(null=True)
    #if the participant arrives late, after the window_end (ie actual_date > window_end) or if the participant arrives early (ie actual_date < window_start) then the doctor must be able to give a reason as text. This field signifies that
    deviation_reason = models.TextField(blank=True, null=True)
    #the status of the visit
    #scheduled: planned but not done yet, completed: participant has visited (actual_date != NULL), missed: window has passed (current date > window_end)
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('missed', 'Missed')], default="scheduled")


    class Meta:
        #a participant can visit at a single start date only. For eg: if p1 has visit_code of baseline then same p1 can't have a visit_code of month_3
        unique_together = ("participant", "visit_code")
        ordering = ["due_date"]

    def __str__(self):
        return f"{self.participant} - {self.visit_type}"