from django.db import models

# Create your models here.
class Study(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    #the official id for the study. Eg: "AMD-P2-2024". This is the primary key
    protocol_id = models.CharField(max_length=100, unique=True)
    #timestamp of when it was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name