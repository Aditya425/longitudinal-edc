from django.urls import path
from . import views

urlpatterns = [
    path("", views.study_dashboard, name="study_dashboard"),
    path("create/", views.create_study, name='create_study'),
    path("<int:study_id>/", views.study_detail, name="study_detail"),
    path("<int:study_id>/add/", views.add_participant, name="add_participant"),
    path("<int:study_id>/edit/", views.edit_study, name="edit_study"),
    path("<int:study_id>/delete/", views.delete_study, name="delete_study"),
    path("<int:study_id>/participants/<int:participant_id>/delete/", views.delete_participant, name="delete_participant"),
]