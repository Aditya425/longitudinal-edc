from django.shortcuts import render
from django.core.paginator import Paginator

from .models import AuditLog


def audit_log_list(request):
    logs = AuditLog.objects.all().order_by("-timestamp")

    action_filter = request.GET.get("action")
    if action_filter:
        logs = logs.filter(action=action_filter)

    paginator = Paginator(logs, 50)
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)

    return render(request, "audit/list.html", {
        "page_obj": page_obj,
        "action_filter": action_filter,
    })
