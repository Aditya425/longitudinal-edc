from django.shortcuts import render, get_object_or_404, redirect
from apps.forms.models import FormTemplate, FormResponse
from apps.participants.models import Visit

# Create your views here.
def fill_form(request, visit_id, template_id):
    #we need visit_id so that we can connect the visit of the user to the form filled by the user.
    #we need template_id to fetch the actual form from FormTemplate
    visit = get_object_or_404(Visit, id=visit_id)
    template = get_object_or_404(FormTemplate, id=template_id)

    #schema contains details of the fields in the form
    schema = template.schema_json["fields"]

    if request.method == 'POST':
        #the answers, user has submitted
        answers = {}

        for field in schema:
            answers[field['name']] = request.POST.get(field['name'])
            #save the answers given by user into FormResponse
        FormResponse.objects.create(
            visit=visit,
            template=template,
            answers_json=answers,
            completed_by=request.user if request.user.is_authenticated else None,
            version=template.version
        )

        return redirect("visit_detail", visit_id=visit.id)
    
    return render(request, "forms/fill_form.html", {"visit": visit, "template": template, "schema": schema})
