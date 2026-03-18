from django.urls import path
from .views import participants_list

urlpatterns = [
    path("studies/<int:study_id>/participants", participants_list, name='participants_list')
]

