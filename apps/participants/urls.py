from django.urls import path
from .views import *

urlpatterns = [
    # path("studies/<int:study_id>/participants", participants_list, name='participants_list'),
    # path('visits/<int:visit_id>/', visit_detail, name='visit_detail')
    # path("<int:study_id>", participants_list, name='participants_list'),
    path("visits/<int:visit_id>", visit_detail, name='visit_detail'),
]

