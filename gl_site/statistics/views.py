# View imports
from django.http import JsonResponse
from django.shortcuts import render
from gl_site.custom_auth import login_required

# Forms
from gl_site.statistics.statistics_form import  statistics_request_form

# Models
from gl_site.models import Organization, Session, Metric

# Inventories
from gl_site.inventories import inventory_by_id

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

                return JsonResponse(data)
            except LookupError as e:
                return JsonResponse([str(e)], status=400, safe=False)

    return JsonResponse(["Method not allowed"], status=405, safe=False)

def generate_data_from_sessions(sessions):
    """ Generate the data dict used to render the graphs """

    # Get all metrics belonging to users
    # registered for each session in sessions
    metrics = Metric.objects.filter(submission__user__leaduserinfo__session__in=sessions)

    # Data set to be returned
    data = {}

    # Process all metrics
    metric_id = 0 # Unique anonymous id for each metric
    for metric in metrics:
        # Inventory the metric belongs to
        inventory_cls = inventory_by_id[metric.submission.inventory_id]
        inventory_name = inventory_cls.__name__

        # If the inventory does not yet exist in the returned data set, add it
        if (inventory_name not in data):
            data[inventory_name] = []

        # Append the value to the data set
        data[inventory_name].append({
            "name": ("Metric-{}".format(metric_id)),
            "key": metric.key,
            "value": metric.value
        })

        # Increment id
        metric_id += 1

    return data
