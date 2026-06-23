from django.test import TestCase, Client
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from apps.studies.models import Study
from apps.participants.models import Participant, Visit
from apps.participants.signals import create_visits_for_new_participant
from .models import FormTemplate, FormResponse


class FormModelTest(TestCase):
    def setUp(self):
        post_save.disconnect(create_visits_for_new_participant, sender=Participant)
        self.template = FormTemplate.objects.create(
            name="Baseline Intake",
            schema_json={"fields": [
                {"name": "age", "label": "Age", "type": "number"},
                {"name": "notes", "label": "Notes", "type": "text"},
            ]}
        )

    def test_template_str(self):
        self.assertEqual(str(self.template), "Baseline Intake")

    def test_form_response_str(self):
        study = Study.objects.create(name="Test", protocol_id="T-001")
        p = Participant.objects.create(
            study=study, participant_code="P-001", enrolled_at=date(2026, 1, 1)
        )
        v = Visit.objects.create(
            participant=p, visit_code="baseline", due_date=date(2026, 1, 1)
        )
        user = User.objects.create_user("doc")
        response = FormResponse.objects.create(
            visit=v, template=self.template,
            answers_json={"age": "30", "notes": "OK"},
            completed_by=user, version=1
        )
        self.assertIn("Baseline Intake", str(response))


class FormViewsTest(TestCase):
    def setUp(self):
        post_save.disconnect(create_visits_for_new_participant, sender=Participant)
        self.client = Client()
        self.template = FormTemplate.objects.create(
            name="Test Form",
            schema_json={"fields": [
                {"name": "field1", "label": "Field 1", "type": "text"},
            ]}
        )
        study = Study.objects.create(name="Test", protocol_id="T-001")
        p = Participant.objects.create(
            study=study, participant_code="P-001", enrolled_at=date(2026, 1, 1)
        )
        self.visit = Visit.objects.create(
            participant=p, visit_code="baseline", due_date=date(2026, 1, 1)
        )

    def test_fill_form_get(self):
        response = self.client.get(
            reverse("fill_form", args=[self.visit.id, self.template.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Form")

    def test_fill_form_post(self):
        response = self.client.post(
            reverse("fill_form", args=[self.visit.id, self.template.id]),
            {"field1": "hello"}
        )
        self.assertRedirects(response, reverse("visit_detail", args=[self.visit.id]))
        self.assertEqual(FormResponse.objects.count(), 1)
