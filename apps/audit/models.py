from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class AuditLog(models.Model):
    #which user performed the action. To get the User class, we use the `get_user_model` function
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    #the action which was taken for this particular activity. The supported values are: CREATE, UPDATE, DELETE, EXPORT, LOGIN, SUBMIT_FORM
    action = models.CharField(max_length=50)
    #the model name on which the action was taken
    model_name = models.CharField(max_length=100)
    #the id of the object on which the action was performed on.
    object_id = models.CharField(max_length=50)
    #the timestamp of this log (also the action as the log happens when the action is taken)
    timestamp = models.DateTimeField(auto_now_add=True)
    #extra info about the action taken as a json
    metadata = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.action} {self.model_name} {self.object_id}"