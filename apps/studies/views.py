from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.utils import IntegrityError
from django.http import HttpResponse
from .models import Study
from apps.participants.models import Visit, Participant

# Create your views here.

#shows all the studies
def study_dashboard(request):
    #get the queryset of all the studies in descending order of created_at
    studies = Study.objects.all().order_by("-created_at")

    #get the search query from the GET url. the query will be "<url>?q=<search-term>"
    query = request.GET.get('q')
    #filter the studies list above to match the query only if query is not an empty string
    if query:
        #search for the rows whose name contains <query>
        studies = studies.filter(name__icontains=query)
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
        completion_rate = None
        if total_visits > 0:
            completion_rate = round((completed_visits / total_visits) * 100, 1)

        #calculating no. of overdue visits. If a visit's status is "scheduled" and current date is greater than the window_end date then it means that the visit is overdue
        overdue_visits = Visit.objects.filter(status="scheduled",window_end__lt=timezone.now().date()).count()
        
        #create a dict of this data and append to our list
        dashboard_data.append({
            "study": study,
            "participant_count": participants_count,
            "total_visits": total_visits,
            "completed_visits": completed_visits,
            "completion_rate": completion_rate,
            "overdue_visits": overdue_visits
        })

    return render(request, "studies/dashboard.html", {"dashboard_data": dashboard_data})

def study_detail(request, study_id):
    #pk is the primary key of the study clicked by the user
    study = get_object_or_404(Study, pk=study_id)
    #get all the participants for this study
    participants = study.participants.all()
    return render(request, 'studies/detail.html', {"study": study, "participants": participants})

def create_study(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        protocol_id = request.POST.get('protocol_id')

        if name and protocol_id:
            Study.objects.create(name=name, description=description, protocol_id=protocol_id)
            return redirect('study_dashboard')
    
    return render(request, 'studies/create.html')

def add_participant(request, study_id):
    study = get_object_or_404(Study, id=study_id)
    if request.method == "POST":
        try:
            Participant.objects.create(
                study=study,
                participant_code=request.POST["participant_code"],
                birth_year=request.POST.get("birth_year") or None,
                sex=request.POST.get("sex"),
                enrolled_at=request.POST["enrolled_at"],
            )
        except IntegrityError:
            return render(request, "studies/add_participant.html", {"study": study, 'error': True})

        return redirect("study_detail", study_id=study.id)

    return render(request, "studies/add_participant.html", {"study": study, 'error': False})