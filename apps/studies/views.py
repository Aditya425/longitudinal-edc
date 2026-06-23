from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Study, VisitType
from apps.participants.models import Visit, Participant


def study_dashboard(request):
    studies = Study.objects.all().order_by("-created_at")

    query = request.GET.get('q')
    if query:
        studies = studies.filter(name__icontains=query)

    dashboard_data = []
    total_participants = 0
    total_overdue = 0

    for study in studies:
        participants_count = study.participants.count()
        total_participants += participants_count
        total_visits = Visit.objects.filter(participant__study=study).count()
        completed_visits = Visit.objects.filter(participant__study=study, status="completed").count()
        completion_rate = None
        if total_visits > 0:
            completion_rate = round((completed_visits / total_visits) * 100, 1)
        overdue_visits = Visit.objects.filter(
            status="scheduled", window_end__lt=timezone.now().date(),
            participant__study=study
        ).count()
        total_overdue += overdue_visits
        dashboard_data.append({
            "study": study,
            "participant_count": participants_count,
            "total_visits": total_visits,
            "completed_visits": completed_visits,
            "completion_rate": completion_rate,
            "overdue_visits": overdue_visits,
        })

    paginator = Paginator(dashboard_data, 10)
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)

    return render(request, "studies/dashboard.html", {
        "page_obj": page_obj,
        "total_studies": Study.objects.count(),
        "total_participants": total_participants,
        "total_overdue": total_overdue,
    })


def study_detail(request, study_id):
    study = get_object_or_404(Study, pk=study_id)
    participants = study.participants.all().order_by("participant_code")

    paginator = Paginator(participants, 20)
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)

    visit_types = study.visit_types.all()

    for p in page_obj:
        p.visit_count = p.visits.count()
        p.completed_visits = p.visits.filter(status="completed").count()

    return render(request, 'studies/detail.html', {
        "study": study,
        "page_obj": page_obj,
        "visit_types": visit_types,
    })


def create_study(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        protocol_id = request.POST.get('protocol_id')

        if name and protocol_id:
            study = Study.objects.create(name=name, description=description or "", protocol_id=protocol_id)

            for vt in ['baseline', 'month_3', 'year_1']:
                target_day = request.POST.get(f"{vt}_target")
                win_before = request.POST.get(f"{vt}_before", 0)
                win_after = request.POST.get(f"{vt}_after", 0)
                if target_day:
                    VisitType.objects.create(
                        study=study,
                        visit_code=vt,
                        target_day=int(target_day),
                        window_before=int(win_before),
                        window_after=int(win_after),
                    )

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


def edit_study(request, study_id):
    study = get_object_or_404(Study, id=study_id)
    if request.method == "POST":
        study.name = request.POST.get("name", study.name)
        study.description = request.POST.get("description", study.description)
        study.protocol_id = request.POST.get("protocol_id", study.protocol_id)
        study.save()

        for vt in study.visit_types.all():
            target_day = request.POST.get(f"{vt.visit_code}_target")
            win_before = request.POST.get(f"{vt.visit_code}_before")
            win_after = request.POST.get(f"{vt.visit_code}_after")
            if target_day:
                vt.target_day = int(target_day)
                vt.window_before = int(win_before) if win_before else 0
                vt.window_after = int(win_after) if win_after else 0
                vt.save()

        return redirect("study_detail", study_id=study.id)

    return render(request, "studies/edit.html", {"study": study})


def delete_study(request, study_id):
    study = get_object_or_404(Study, id=study_id)
    if request.method == "POST":
        study.delete()
        return redirect("study_dashboard")
    return render(request, "studies/confirm_delete.html", {"object": study, "type": "Study"})


def delete_participant(request, study_id, participant_id):
    participant = get_object_or_404(Participant, id=participant_id, study_id=study_id)
    if request.method == "POST":
        participant.delete()
        return redirect("study_detail", study_id=study_id)
    return render(request, "studies/confirm_delete.html", {
        "object": participant,
        "type": "Participant",
        "cancel_url": "study_detail",
        "cancel_arg": study_id,
    })
