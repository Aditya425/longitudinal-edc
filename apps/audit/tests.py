from django.test import TestCase
from django.contrib.auth.models import User
from .models import AuditLog
from .services import log_action


class AuditLogTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("admin", password="pass")

    def test_log_action(self):
        log_action(self.user, "CREATE", "Study", 1, {"name": "Test"})
        self.assertEqual(AuditLog.objects.count(), 1)
        entry = AuditLog.objects.first()
        self.assertEqual(entry.action, "CREATE")
        self.assertEqual(entry.model_name, "Study")
        self.assertEqual(entry.user, self.user)

    def test_log_action_no_user(self):
        log_action(None, "EXPORT", "ExportJob", 5)
        self.assertEqual(AuditLog.objects.count(), 1)
        entry = AuditLog.objects.first()
        self.assertIsNone(entry.user)
        self.assertEqual(entry.action, "EXPORT")
