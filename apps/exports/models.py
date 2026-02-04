from django.db import models

# Create your models here.
class ExportJob(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("running", "Running"),
        ("completed", "Completed"),
        ("failed", "Failed")
    ]
    #a fixed set of allowed states for a export job
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    #when the job was created
    created_at = models.DateTimeField(auto_now_add=True)
    #when the job is completed (success or failure)
    completed_at = models.DateTimeField(null=True, blank=True)
    #a human readable message as to why the job failed (if there is failure)
    error_message = models.TextField(blank=True)

