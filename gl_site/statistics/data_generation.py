# Models
from gl_site.models import Metric, Submission, Organization, Session

# Inventories
from gl_site.inventories import inventory_by_id
from gl_site.inventories.via import Via

from . import via_inverse

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

def generate_data_from_sessions(sessions):
    """ Generate the data dict used to render the graphs """

    # Get all metrics belonging to users
    # registered for each session in sessions.
    # Exclude Via. It is processed separately for simplicity.
    metrics = Metric.objects.filter(
        submission__user__leaduserinfo__session__in=sessions
    ).exclude(
        submission__inventory_id=Via.inventory_id
    )

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

    # Via data
    via_data = {}

    # Get all via Submissions
    submissions = Submission.objects.filter(inventory_id=Via.inventory_id)

    # Process each submission
    for submission in submissions:
        # Get the associated metrics and process them
        strengths = {}
        metrics = Metric.objects.filter(submission=submission)
        Via().review_process_metrics(strengths, metrics)

        # Process the strengths
        for strength in strengths['strengths']:
            if (strength['is_signature']):
                name = strength['strength']
                if (name not in via_data):
                    via_data[name] = {}
                    via_data[name]['value'] = 0

                via_data[name]['value'] += 1

    # Add the via data
    data[Via.__name__] = []
    for key, value in via_data.items():
        value['name'] = via_inverse[key] # Via category
        value['key'] = key
        data[Via.__name__].append(value)

    # Return an ordered list
    data_list = []
    for key, value in data.items():
        data_list.append({'inventory': key, 'data': value})
    data_list = sorted(data_list, key=lambda k: k['inventory'])

    return data_list
