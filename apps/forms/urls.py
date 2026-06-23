from django.urls import path
from . import views

urlpatterns = [
    path("<int:visit_id>/<int:template_id>/", views.fill_form, name="fill_form"),
    path("responses/<int:response_id>/", views.view_form_response, name="view_form_response"),
]