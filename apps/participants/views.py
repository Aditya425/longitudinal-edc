from django.shortcuts import render, get_object_or_404
from apps.studies.models import Study
from .models import Participant

# Create your views here.
def participants_list(request, study_id):
    #get the study object from the study id
    study = get_object_or_404(Study, id=study_id)
    #get the participants related to the study
    participants = Participant.objects.filter(study=study).order_by('participant_code')
    return render(request, 'participants/list.html', {'study': study, 'participants': participants})