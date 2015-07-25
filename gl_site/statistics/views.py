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

    querysets = get_queryset(request)

    form = statistics_request_form(
        querysets['organizations'],
        querysets['sessions'],
        request.POST
    )

    if (form.is_valid()):
        return JsonResponse({
            'organization': form.cleaned_data['organization'].name,
            'session': form.cleaned_data['session'].name
        })

    return JsonResponse({})
