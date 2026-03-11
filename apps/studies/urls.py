from django.urls import path
from .views import study_dashboard, study_detail

urlpatterns = [
    path("", study_dashboard, name="study_dashboard"),
    path("<int:pk>", study_detail, name="study_detail")
]