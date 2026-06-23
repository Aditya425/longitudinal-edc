from django.urls import path
from . import views

urlpatterns = [
    path("", views.export_list, name="export_list"),
    path("create/", views.create_export, name="create_export"),
    path("<int:job_id>/download/", views.download_export, name="download_export"),
]
