from datetime import timedelta, datetime
from .models import Visit
from apps.studies.models import VisitType


def schedule_visits_for_participant(participant, visit_defs=None):
    if visit_defs is None:
        visit_defs_qs = VisitType.objects.filter(study=participant.study).values(
            "visit_code", "target_day", "window_before", "window_after"
        )
        visit_defs = list(visit_defs_qs)

    if not visit_defs:
        from .protocol import VISIT_SCHEDULE
        visit_defs = VISIT_SCHEDULE

    baseline_date = participant.enrolled_at
    if isinstance(baseline_date, str):
        baseline_date = datetime.strptime(baseline_date, "%Y-%m-%d")

    if participant.visits.exists():
        return

    visits = []
    for v in visit_defs:
        due_date = baseline_date + timedelta(days=v["target_day"])
        visits.append(
            Visit(
                participant=participant,
                visit_code=v["visit_code"],
                due_date=due_date,
                window_start=due_date - timedelta(days=v.get("window_before", 0)),
                window_end=due_date + timedelta(days=v.get("window_after", 0)),
                status="scheduled",
                actual_date=None,
            )
        )

    Visit.objects.bulk_create(visits)
