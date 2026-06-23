from rest_framework import serializers
from .models import Participant, Visit, VisitDeviation


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ["id", "participant", "visit_code", "actual_date", "due_date",
                   "window_start", "window_end", "deviation_reason", "status"]


class ParticipantSerializer(serializers.ModelSerializer):
    visits = VisitSerializer(many=True, read_only=True)

    class Meta:
        model = Participant
        fields = ["id", "study", "participant_code", "birth_year", "sex", "enrolled_at", "visits"]
