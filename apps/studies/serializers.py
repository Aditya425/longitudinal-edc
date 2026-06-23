from rest_framework import serializers
from .models import Study, VisitType


class VisitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitType
        fields = ["id", "visit_code", "target_day", "window_before", "window_after", "required"]


class StudySerializer(serializers.ModelSerializer):
    visit_types = VisitTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Study
        fields = ["id", "name", "description", "protocol_id", "created_at", "visit_types"]
