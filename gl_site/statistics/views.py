# View imports
from django.http import JsonResponse
from django.shortcuts import render
from gl_site.custom_auth import login_required

# Forms
from gl_site.statistics.statistics_form import  statistics_request_form

# Models
from gl_site.models import Organization, Session

def get_queryset(request):
    """ Non view helper function for returning proper querysets """
    # Get the list of organizations the user can view data for.
    if (request.user.is_staff):
        organizations = Organization.objects.all()
    else:
        organizations = Organization.objects.filter(id=request.user.leaduserinfo.organization.id)

    # Load all sessions belonging to the organizations
    sessions = Session.objects.filter(organization__in = organizations)

    return {'organizations': organizations, 'sessions': sessions}

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
                # and the user is staff, load data for all organizations.
                if (request.user.is_staff and form.cleaned_data['organization'] is None):
                    organizations = Organization.objects.all()
                # Load the user's organization.
                else:
                    organizations = [form.cleaned_data['organization']]

                # If session is not explicitly defined
                # load data for all sessions
                if (form.cleaned_data['session'] is None):
                    sessions = Session.objects.filter(organization__in = organizations)
                else:
                    if (form.cleaned_data['session'].organization not in organizations):
                        raise LookupError("Invalid session selection")
                    sessions = [form.cleaned_data['session']]
            except LookupError:
                return JsonResponse(["Invalid parameters"], status=400, safe=False)

            return JsonResponse({
                'organizations': [org.name for org in organizations],
                'sessions': [session.name for session in sessions]
            })

    return JsonResponse(["Method not allowed"], status=405, safe=False)
