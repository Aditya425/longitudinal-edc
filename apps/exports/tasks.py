import csv
import os
import io
from datetime import datetime

from celery import shared_task
from django.conf import settings

from .models import ExportJob


@shared_task
def run_export_job(job_id):
    try:
        job = ExportJob.objects.get(pk=job_id)
        job.status = "running"
        job.save()

        from apps.participants.models import Visit, Participant

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Participant Code", "Study", "Visit Code", "Due Date",
            "Window Start", "Window End", "Actual Date", "Status", "Deviation Reason"
        ])

        visits = Visit.objects.select_related("participant__study").all()
        if job.study_id:
            visits = visits.filter(participant__study=job.study_id)

        for v in visits:
            writer.writerow([
                v.participant.participant_code,
                v.participant.study.protocol_id,
                v.visit_code,
                v.due_date,
                v.window_start,
                v.window_end,
                v.actual_date or "",
                v.status,
                v.deviation_reason or "",
            ])

        export_dir = os.path.join(settings.BASE_DIR, "exports")
        os.makedirs(export_dir, exist_ok=True)
        filename = f"export_{job.pk}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(export_dir, filename)

        with open(filepath, "w", newline="") as f:
            f.write(output.getvalue())

        job.status = "completed"
        job.completed_at = datetime.now()
        job.file_path = filepath
        job.save()

    except Exception as e:
        job.status = "failed"
        job.completed_at = datetime.now()
        job.error_message = str(e)
        job.save()
