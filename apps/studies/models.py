from django.db import models


class Study(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    protocol_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class VisitType(models.Model):
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name="visit_types")
    visit_code = models.CharField(max_length=20)
    target_day = models.IntegerField()
    window_before = models.IntegerField(default=0)
    window_after = models.IntegerField(default=0)
    required = models.BooleanField(default=True)

    class Meta:
        unique_together = ("study", "visit_code")

    def __str__(self):
        return f"{self.study.protocol_id} - {self.visit_code}"