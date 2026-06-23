import os

from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponseNotFound
from django.core.paginator import Paginator
from django.contrib import messages

from .models import ExportJob
from .tasks import run_export_job
from apps.studies.models import Study


def export_list(request):
    jobs = ExportJob.objects.all().order_by("-created_at")
    paginator = Paginator(jobs, 20)
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)
    studies = Study.objects.all()
    return render(request, "exports/list.html", {
        "page_obj": page_obj,
        "studies": studies,
    })


def create_export(request):
    if request.method == "POST":
        study_id = request.POST.get("study_id")
        job = ExportJob.objects.create(
            export_type="visits",
            study_id=study_id if study_id else None,
            created_by=request.user if request.user.is_authenticated else None,
            status="pending",
        )
        run_export_job.delay(job.pk)
        return redirect("export_list")
    return redirect("export_list")


def download_export(request, job_id):
    job = get_object_or_404(ExportJob, pk=job_id)
    if job.status != "completed" or not job.file_path:
        return HttpResponseNotFound("Export not ready or missing file.")
    if os.path.exists(job.file_path):
        return FileResponse(open(job.file_path, "rb"), as_attachment=True, filename=os.path.basename(job.file_path))
    return HttpResponseNotFound("File not found.")
