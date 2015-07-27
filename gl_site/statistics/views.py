# View imports
from django.http import JsonResponse
from django.shortcuts import render
from gl_site.custom_auth import login_required

# Forms
from gl_site.statistics.statistics_form import  statistics_request_form

# Models
from gl_site.models import Organization, Session

# Data
from .data_generation import generate_data_from_sessions, get_queryset

@login_required
def view_statistics(request):
    """ View responsable for initially loading the statistics page """

    # Get the proper queryset and generate the form
    querysets = get_queryset(request)
    form = statistics_request_form(
        querysets['organizations'],
        querysets['sessions']
    )
    return render(request, 'statistics/statistics.html', {'form': form})

@login_required
def load_data(request):
    """ Returns a JSON respons containing statistics data """

    if (request.method == 'GET'):
        # Get the querysets accessable by the user
        querysets = get_queryset(request)

        # Build the submitted form from request data
        form = statistics_request_form(
            querysets['organizations'],
            querysets['sessions'],
            request.GET
        )

        # Validate the form
        if (form.is_valid()):
            try:
                # If organization is not explicitly defined
                if (form.cleaned_data['organization'] is None):
                    # The user is staff, load data for all organizations.
                    if (request.user.is_staff):
                        organizations = Organization.objects.all()
                    # The user is not staff, load their organization.
                    else:
                        organizations = [request.user.leaduserinfo.organization]
                # Load the selected organization
                else:
                    # Verify the user has the permissions for the requested organization
                    if (not request.user.is_staff and
                        form.cleaned_data['organization'] != request.user.leaduserinfo.organization):

                        raise LookupError("Invalid organization selection")
                    organizations = [form.cleaned_data['organization']]

                # If session is not explicitly defined
                # load data for all sessions
                if (form.cleaned_data['session'] is None):
                    sessions = Session.objects.filter(organization__in = organizations)
                else:
                    if (form.cleaned_data['session'].organization not in organizations):
                        raise LookupError("Invalid session selection")
                    sessions = [form.cleaned_data['session']]


                data = generate_data_from_sessions(sessions)

                return JsonResponse(data, safe=False)
            except LookupError as e:
                return JsonResponse([str(e)], status=400, safe=False)

    return JsonResponse(["Method not allowed"], status=405, safe=False)
