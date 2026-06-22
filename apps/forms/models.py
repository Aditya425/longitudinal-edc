from django.db import models
from django.contrib.auth import get_user_model
from apps.participants.models import Visit

User = get_user_model()
# Create your models here.
#This stores the name of all the forms in our system and its fields. Its basically a table of the available forms
class FormTemplate(models.Model):
    #the name of the form (eg: Follow up visit, Baseline intake etc.)
    name = models.CharField(max_length=255)
    #the name of the fields present in this form. It looks like this: 
    # schema_json = {
            #"fields" is a list of all the fields present in this form
    #     fields = [
        #here "name" is name of the field in the db, "label" is what we display in ui, "type" is data type
    #         {"name": "age", "label": "Age", "type": "number"},
    #         {"name": "weight", "label": "Weight", "type": "number"},
    #         {"name": "notes", "label": "Notes", "type": "text"},
    #     ]
    # }
    schema_json = models.JSONField()
    #the version of the form. By default it is 1. If we change the form (ie adding or removing some fields, changing data type of fields etc) then we'll increment the version
    version = models.IntegerField(default=1)

    def __str__(self):
        return self.name
    
#this stores the form responses
class FormResponse(models.Model):
    #the visit for which this form is made for
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name="forms")
    #the form for which its being responded ie the form currently being filled
    template = models.ForeignKey(FormTemplate, on_delete=models.CASCADE)
    #the form responses by user will be in the form of json so we use a JSONField() which will serialize the json automatically
    answers_json = models.JSONField()
    #the doctor who filled this form. Since the doctor is the current user of this website, we get the current user by doing get_user_model()
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    #the form created date
    completed_at = models.DateTimeField(auto_now_add=True)
    #the version of this response. If the participant response changes then this will be incremented.
    version = models.IntegerField()

    def __str__(self):
        return f"{self.form_name} ({self.visit})"