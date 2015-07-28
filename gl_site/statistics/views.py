# View imports
from django.http import JsonResponse
from django.shortcuts import render
from gl_site.custom_auth import login_required

# Forms
from gl_site.statistics.statistics_form import  statistics_request_form

# Data
from .data_generation import generate_data_from_sessions, get_queryset, validate_sessions

# Response statuses
BAD_REQUEST = 400
FORBIDDEN = 403
METHOD_NOT_ALLOWED = 405

# Error messages
METHOD_NOT_ALLOWED_MESSAGE = "Method not allowed."
INVALID_DATA_SELECTION = "Invalid data selection."

@login_required
def view_statistics(request):
    """ View responsable for initially loading the statistics page """

    # Get the proper queryset and generate the form
    querysets = get_queryset(request.user)
    form = statistics_request_form(
        querysets['organizations'],
        querysets['sessions']
    )
    return render(request, 'statistics/statistics.html', {'form': form})

@login_required
def load_data(request):
    """ Returns a JSON respons containing statistics data """

    # Deny non GET requests
    if (request.method != 'GET'):
        return JsonResponse([METHOD_NOT_ALLOWED_MESSAGE], status=METHOD_NOT_ALLOWED, safe=False)

    # Get the querysets accessable by the user
    querysets = get_queryset(request.user)

    # Build the submitted form from request data
    form = statistics_request_form(
        querysets['organizations'],
        querysets['sessions'],
        request.GET
    )

    # Validate the form
    if (not form.is_valid()):
        return JsonResponse([INVALID_DATA_SELECTION], status=FORBIDDEN, safe=False)

    try:
        # Validate sessions
        sessions = validate_sessions(
            form.cleaned_data['organization'],
            form.cleaned_data['session'],
            request.user
        )

        # Generate the data
        data = generate_data_from_sessions(sessions, request.user)

        # Return the JSON encoded response
        return JsonResponse(data, safe=False)
    except LookupError as e:
        return JsonResponse([str(e)], status=BAD_REQUEST, safe=False)
