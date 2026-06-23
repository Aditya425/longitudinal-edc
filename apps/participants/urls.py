from django.urls import path
from . import views

urlpatterns = [
    path("<int:study_id>/", views.participants_list, name='participants_list'),
    path("<int:study_id>/<int:participant_id>/edit/", views.edit_participant, name='edit_participant'),
    path("<int:study_id>/<int:participant_id>/delete/", views.delete_participant, name='delete_participant'),
    path("visits/<int:visit_id>/", views.visit_detail, name='visit_detail'),
]
