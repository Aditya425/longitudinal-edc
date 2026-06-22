from django.urls import path
from .views import *

urlpatterns = [
    path("", study_dashboard, name="study_dashboard"),
    path("<int:study_id>/", study_detail, name="study_detail"),
    path("<int:study_id>/add/", add_participant, name="add_participant"),
    path("create", create_study, name='create_study')
]