from django.urls import path
from .views import study_dashboard

urlpatterns = [
    path("", study_dashboard, name="study_dashboard")
]