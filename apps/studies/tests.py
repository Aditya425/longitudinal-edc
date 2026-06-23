from django.test import TestCase, Client
from django.urls import reverse
from .models import Study, VisitType


class StudyModelTest(TestCase):
    def setUp(self):
        self.study = Study.objects.create(
            name="Test Study", protocol_id="TEST-001", description="Desc"
        )

    def test_study_str(self):
        self.assertEqual(str(self.study), "Test Study")

    def test_visit_type_creation(self):
        vt = VisitType.objects.create(
            study=self.study, visit_code="month_1", target_day=30,
            window_before=5, window_after=5
        )
        self.assertEqual(str(vt), "TEST-001 - month_1")
        self.assertEqual(vt.target_day, 30)


class StudyViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.study = Study.objects.create(
            name="Test Study", protocol_id="TEST-001", description="Desc"
        )
        VisitType.objects.create(
            study=self.study, visit_code="baseline", target_day=0,
            window_before=0, window_after=0
        )

    def test_dashboard(self):
        response = self.client.get(reverse("study_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Study")

    def test_create_study_get(self):
        response = self.client.get(reverse("create_study"))
        self.assertEqual(response.status_code, 200)

    def test_create_study_post(self):
        response = self.client.post(reverse("create_study"), {
            "name": "New Study", "protocol_id": "NEW-001",
            "baseline_target": 0,
        })
        self.assertRedirects(response, reverse("study_dashboard"))
        self.assertEqual(Study.objects.count(), 2)

    def test_detail(self):
        response = self.client.get(reverse("study_detail", args=[self.study.id]))
        self.assertEqual(response.status_code, 200)

    def test_edit_study(self):
        response = self.client.post(reverse("edit_study", args=[self.study.id]), {
            "name": "Updated", "protocol_id": "TEST-001",
        })
        self.assertRedirects(response, reverse("study_detail", args=[self.study.id]))
        self.study.refresh_from_db()
        self.assertEqual(self.study.name, "Updated")

    def test_delete_study_get(self):
        response = self.client.get(reverse("delete_study", args=[self.study.id]))
        self.assertEqual(response.status_code, 200)

    def test_delete_study_post(self):
        response = self.client.post(reverse("delete_study", args=[self.study.id]))
        self.assertRedirects(response, reverse("study_dashboard"))
        self.assertEqual(Study.objects.count(), 0)
