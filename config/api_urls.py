from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.studies.api import StudyViewSet
from apps.participants.api import ParticipantViewSet, VisitViewSet
from apps.forms.api import FormTemplateViewSet, FormResponseViewSet

router = DefaultRouter()
router.register(r"studies", StudyViewSet)
router.register(r"participants", ParticipantViewSet)
router.register(r"visits", VisitViewSet)
router.register(r"form-templates", FormTemplateViewSet)
router.register(r"form-responses", FormResponseViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
