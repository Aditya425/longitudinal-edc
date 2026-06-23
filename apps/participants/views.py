from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.utils import IntegrityError
from django.contrib import messages

from apps.studies.models import Study
from apps.forms.models import FormTemplate, FormResponse
from .models import Participant, Visit, VisitDeviation
from datetime import datetime


def participants_list(request, study_id):
    study = get_object_or_404(Study, id=study_id)
    participants = Participant.objects.filter(study=study).order_by('participant_code')

    query = request.GET.get('q')
    if query:
        participants = participants.filter(participant_code__icontains=query)

    status_filter = request.GET.get('status')
    if status_filter:
        participants = participants.filter(
            visits__status=status_filter
        ).distinct()

    paginator = Paginator(participants, 20)
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)

    return render(request, 'participants/list.html', {
        'study': study,
        'page_obj': page_obj,
    })


def visit_detail(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    error = None

    if request.method == 'POST':
        actual_date = request.POST.get('actual_date')
        deviation_reason = request.POST.get('deviation_reason')

        if actual_date:
            actual_date = datetime.strptime(actual_date, "%Y-%m-%d").date()

            if actual_date < visit.window_start or actual_date > visit.window_end:
                if not deviation_reason:
                    error = "Deviation reason is required (visit outside allowed window)"
                else:
                    visit.deviation_reason = deviation_reason
                    VisitDeviation.objects.update_or_create(
                        visit=visit,
                        defaults={"reason": deviation_reason, "created_by": request.user if request.user.is_authenticated else None},
                    )

            visit.actual_date = actual_date
            visit.status = "completed"

            if not error:
                visit.save()
                return redirect("visit_detail", visit.id)

    templates = FormTemplate.objects.all()
    existing_forms = visit.forms.select_related("template").all()

    return render(request, 'participants/visit_detail.html', {
        'visit': visit,
        'error': error,
        'templates': templates,
        'existing_forms': existing_forms,
    })


def edit_participant(request, study_id, participant_id):
    study = get_object_or_404(Study, id=study_id)
    participant = get_object_or_404(Participant, id=participant_id, study=study)

    if request.method == "POST":
        try:
            participant.participant_code = request.POST.get("participant_code", participant.participant_code)
            participant.birth_year = request.POST.get("birth_year") or None
            participant.sex = request.POST.get("sex", participant.sex)
            participant.enrolled_at = request.POST.get("enrolled_at", participant.enrolled_at)
            participant.save()
            return redirect("participants_list", study_id=study.id)
        except IntegrityError:
            return render(request, "participants/edit.html", {
                "study": study, "participant": participant, "error": True
            })

    return render(request, "participants/edit.html", {
        "study": study, "participant": participant, "error": False
    })


def delete_participant(request, study_id, participant_id):
    participant = get_object_or_404(Participant, id=participant_id, study_id=study_id)
    if request.method == "POST":
        participant.delete()
        return redirect("participants_list", study_id=study_id)
    return render(request, "participants/confirm_delete.html", {
        "object": participant, "type": "Participant",
        "cancel_url": "participants_list", "cancel_arg": study_id,
    })
