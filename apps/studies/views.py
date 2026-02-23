from django.shortcuts import render
from .models import Study
from apps.participants.models import Visit

# Create your views here.

#shows all the studies
def study_dashboard(request):
    #get the queryset of all the studies in descending order of created_at
    studies = Study.objects.all().order_by("-created_at")

    #it contains a list of dictionaries where each dictionary represents a study
    dashboard_data = []

    for study in studies:
        #the count of all the participants under the current study
        participants_count = study.participants.count()
        #here we're calculating the number of rows in visit where the participant has registered for the current study object, in other words, the number of visits by a participant to our clinic where the participant has registered for the current study (which is the current study object 'study')
        #for this we've to filter on visits where the participant's study (in participant table) is equal to study (the current object in for loop)
        total_visits = Visit.objects.filter(participant__study=study).count()
        #of the total visits, how many of them are completed. This variable counts that
        completed_visits = Visit.objects.filter(participant__study=study, status="completed").count()
        #completion percentage
        if total_visits > 0:
            completion_rate = round((completed_visits / total_visits) * 100, 1)
        
        #create a dict of this data and append to our list
        dashboard_data.append({
            "study": study,
            "participant_count": participants_count,
            "total_visits": total_visits,
            "completed_visits": completed_visits,
            "completion_rate": completion_rate
        })

    return render(request, "studies/dashboard.html", {"dashboard_data": dashboard_data})
