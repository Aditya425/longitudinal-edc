from rest_framework import viewsets
from .models import Participant, Visit
from .serializers import ParticipantSerializer, VisitSerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all().order_by("participant_code")
    serializer_class = ParticipantSerializer
    filterset_fields = ["study"]


class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all().order_by("due_date")
    serializer_class = VisitSerializer
    filterset_fields = ["participant", "status"]
