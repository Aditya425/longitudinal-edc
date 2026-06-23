from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from apps.studies.models import Study, VisitType
from .models import Participant, Visit, VisitDeviation
from .services import schedule_visits_for_participant
from .protocol import VISIT_SCHEDULE
from .signals import create_visits_for_new_participant


class ParticipantModelTest(TestCase):
    def setUp(self):
        post_save.disconnect(create_visits_for_new_participant, sender=Participant)
        self.study = Study.objects.create(name="Test", protocol_id="T-001")
        self.participant = Participant.objects.create(
            study=self.study, participant_code="ABC-001",
            enrolled_at=date(2026, 1, 1)
        )

    def test_participant_str(self):
        self.assertEqual(str(self.participant), "T-001 - ABC-001")


class SchedulingTest(TestCase):
    def setUp(self):
        post_save.disconnect(create_visits_for_new_participant, sender=Participant)
        self.study = Study.objects.create(name="Test", protocol_id="T-001")
        VisitType.objects.create(
            study=self.study, visit_code="baseline", target_day=0,
        )
        VisitType.objects.create(
            study=self.study, visit_code="month_3", target_day=90,
            window_before=14, window_after=21
        )

    def test_schedule_visits_from_protocol(self):
        p = Participant.objects.create(
            study=self.study, participant_code="P-001",
            enrolled_at=date(2026, 1, 1)
        )
        schedule_visits_for_participant(p, VISIT_SCHEDULE)
        self.assertEqual(p.visits.count(), 3)
        baseline = p.visits.get(visit_code="baseline")
        self.assertEqual(baseline.due_date, date(2026, 1, 1))
        self.assertEqual(baseline.status, "scheduled")

    def test_schedule_visits_from_db(self):
        p = Participant.objects.create(
            study=self.study, participant_code="P-002",
            enrolled_at=date(2026, 1, 1)
        )
        schedule_visits_for_participant(p)
        self.assertEqual(p.visits.count(), 2)

    def test_schedule_idempotent(self):
        p = Participant.objects.create(
            study=self.study, participant_code="P-003",
            enrolled_at=date(2026, 1, 1)
        )
        schedule_visits_for_participant(p, VISIT_SCHEDULE)
        schedule_visits_for_participant(p, VISIT_SCHEDULE)
        self.assertEqual(p.visits.count(), 3)


class VisitModelTest(TestCase):
    def setUp(self):
        post_save.disconnect(create_visits_for_new_participant, sender=Participant)
        self.user = User.objects.create_user("testuser", password="pass")
        self.study = Study.objects.create(name="Test", protocol_id="T-001")
        self.participant = Participant.objects.create(
            study=self.study, participant_code="P-001",
            enrolled_at=date(2026, 1, 1)
        )
        self.visit = Visit.objects.create(
            participant=self.participant, visit_code="baseline",
            due_date=date(2026, 1, 1), status="scheduled"
        )

    def test_visit_str(self):
        self.assertIn("baseline", str(self.visit))

    def test_visit_deviation(self):
        dev = VisitDeviation.objects.create(
            visit=self.visit, reason="Patient was late",
            created_by=self.user
        )
        self.assertEqual(str(dev), f"Deviation: {self.visit}")
        self.assertEqual(dev.reason, "Patient was late")


class ParticipantViewsTest(TestCase):
    def setUp(self):
        post_save.disconnect(create_visits_for_new_participant, sender=Participant)
        self.client = Client()
        self.study = Study.objects.create(name="Test", protocol_id="T-001")
        self.participant = Participant.objects.create(
            study=self.study, participant_code="P-001",
            enrolled_at=date(2026, 1, 1)
        )

    def test_participants_list(self):
        response = self.client.get(
            reverse("participants_list", args=[self.study.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "P-001")

    def test_edit_participant(self):
        response = self.client.post(
            reverse("edit_participant", args=[self.study.id, self.participant.id]),
            {"participant_code": "P-002", "enrolled_at": "2026-01-15"}
        )
        self.assertRedirects(
            response, reverse("participants_list", args=[self.study.id])
        )
        self.participant.refresh_from_db()
        self.assertEqual(self.participant.participant_code, "P-002")
