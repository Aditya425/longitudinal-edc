from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from apps.forms.models import FormTemplate, FormResponse
from apps.participants.models import Visit


def fill_form(request, visit_id, template_id):
    visit = get_object_or_404(Visit, id=visit_id)
    template = get_object_or_404(FormTemplate, id=template_id)
    schema = template.schema_json["fields"]
    existing = FormResponse.objects.filter(visit=visit, template=template).first()

    if request.method == 'POST':
        answers = {}
        for field in schema:
            val = request.POST.get(field['name'])
            if field.get('type') == 'checkbox':
                val = request.POST.get(field['name']) == 'on'
            answers[field['name']] = val

        if existing:
            existing.answers_json = answers
            existing.version = template.version
            existing.completed_by = request.user if request.user.is_authenticated else None
            existing.save()
        else:
            FormResponse.objects.create(
                visit=visit,
                template=template,
                answers_json=answers,
                completed_by=request.user if request.user.is_authenticated else None,
                version=template.version,
            )

        return redirect("visit_detail", visit_id=visit.id)

    initial = existing.answers_json if existing else {}
    return render(request, "forms/fill_form.html", {
        "visit": visit,
        "template": template,
        "schema": schema,
        "existing": existing,
        "initial": initial,
    })


def view_form_response(request, response_id):
    response = get_object_or_404(FormResponse, id=response_id)
    schema = response.template.schema_json["fields"]
    field_labels = {f["name"]: f["label"] for f in schema}
    return render(request, "forms/view_form.html", {
        "response": response,
        "field_labels": field_labels,
    })
