from rest_framework import viewsets
from .models import Study
from .serializers import StudySerializer


class StudyViewSet(viewsets.ModelViewSet):
    queryset = Study.objects.all().order_by("-created_at")
    serializer_class = StudySerializer
