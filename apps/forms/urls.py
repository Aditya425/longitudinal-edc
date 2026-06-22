from django.urls import path
from apps.forms.views import fill_form

urlpatterns = [
    # path("visits/<int:visit_id>/forms/<int:template_id>", fill_form, name="fill_form")
    path("forms/<int:template_id>", fill_form, name="fill_form")
]