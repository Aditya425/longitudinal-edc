from django.shortcuts import render, get_object_or_404, redirect
from apps.studies.models import Study
from .models import Participant, Visit
from datetime import datetime

# Create your views here.
def participants_list(request, study_id):
    #get the study object from the study id
    study = get_object_or_404(Study, id=study_id)
    #get the participants related to the study
    participants = Participant.objects.filter(study=study).order_by('participant_code')
    return render(request, 'participants/list.html', {'study': study, 'participants': participants})

def visit_detail(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    #if the deviation reason is not given, then return an error message. The variable error is meant for that. By default its none
    error = None
    #this if block says what happens when a participant has visited. If the participant has visited then they'll have an actual date which means we'll change the statud and actual_date in db
    if request.method == 'POST':
        actual_date = request.POST.get('actual_date')
        deviation_reason = request.POST.get('deviation_reason')
        if actual_date:
            #actual_date is a string, convert it to datetime object
            actual_date = datetime.strptime(actual_date, "%Y-%m-%d").date()
            #compare with window start and window end to check whether there is a deviation
            if actual_date < visit.window_start or actual_date > visit.window_end:
                #since there is a deviation, a reason must be given by the user. If not give an error msg
                if not deviation_reason:
                    error = "Deviation reason is required (visit outside allowed window)"
                else:
                    #if deviation reason is already given then just update the visit object
                    visit.deviation_reason = deviation_reason
            
            #since the participant has arrived, update the arrived_date for this visit and assign status as completed
            visit.actual_date = actual_date
            visit.status = "completed"
            #if there is no error, save the form
            if not error:
                visit.save()
                return redirect("visit_detail", visit.id)
    #send the visit and error (if any) back to visit detail page
    return render(request, 'participants/visit_detail.html', {'visit': visit, 'error': error})