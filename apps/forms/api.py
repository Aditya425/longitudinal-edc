from rest_framework import viewsets
from .models import FormTemplate, FormResponse
from .serializers import FormTemplateSerializer, FormResponseSerializer


class FormTemplateViewSet(viewsets.ModelViewSet):
    queryset = FormTemplate.objects.all()
    serializer_class = FormTemplateSerializer


class FormResponseViewSet(viewsets.ModelViewSet):
    queryset = FormResponse.objects.all().order_by("-completed_at")
    serializer_class = FormResponseSerializer
    filterset_fields = ["visit", "template"]
