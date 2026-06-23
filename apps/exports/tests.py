from django.test import TestCase
from .models import ExportJob


class ExportJobModelTest(TestCase):
    def test_create_export_job(self):
        job = ExportJob.objects.create(export_type="visits")
        self.assertEqual(job.status, "pending")
        self.assertIsNone(job.completed_at)
        self.assertEqual(job.file_path, "")

    def test_status_choices(self):
        job = ExportJob.objects.create(export_type="visits", status="running")
        self.assertEqual(job.status, "running")
