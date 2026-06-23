from rest_framework import serializers
from .models import FormTemplate, FormResponse


class FormTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormTemplate
        fields = ["id", "name", "schema_json", "version"]


class FormResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormResponse
        fields = ["id", "visit", "template", "answers_json", "completed_by", "completed_at", "version"]
