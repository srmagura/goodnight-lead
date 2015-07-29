# Models
from gl_site.models import Metric, Submission, Organization, Session

# Inventories
from gl_site.inventories import inventory_by_id, numeric_inventory_cls_list
from gl_site.inventories.via import Via

# Via categories
from gl_site.statistics import via_inverse

# Minimum number of submissions needed to load data
MINIMUM_SUBMISSIONS = 10

# Lookup error messages
INVALID_ORGANIZATION = "Invalid organization selection."
INVALID_SESSION = "Invalid session selection."
NO_DATA = "There were no inventories with sufficient data to display statistics."

def get_queryset(user):
    """ Return proper querysets viewable by a given user """
    # Get the list of organizations the user can view data for.
    if (user.is_staff):
        organizations = Organization.objects.all()
    else:
        organizations = Organization.objects.filter(id=user.leaduserinfo.organization.id)

    # Load all sessions belonging to the organizations
    sessions = Session.objects.filter(organization__in = organizations)

    return {'organizations': organizations, 'sessions': sessions}

def validate_sessions(organization, session, user):
    """ Validate a user's selection of organization and session.
        Returns an iterable containing all sessions.
        Throws an exception if an error occurs.
    """

    # If organization is not explicitly defined
    if (organization is None):
        # The user is staff, load data for all organizations.
        if (user.is_staff):
            organizations = Organization.objects.all()
        # The user is not staff, load their organization.
        else:
            organizations = [user.leaduserinfo.organization]
    # Load the selected organization
    else:
        # Verify the user has the permissions for the requested organization
        if (not user.is_staff and
            organization != user.leaduserinfo.organization):

            raise LookupError(INVALID_ORGANIZATION)
        organizations = [organization]

    # If session is not explicitly defined
    # load data for all sessions
    if (session is None):
        sessions = Session.objects.filter(organization__in = organizations)
    else:
        if (session.organization not in organizations):
            raise LookupError(INVALID_SESSION)
        sessions = [session]

    return sessions

def generate_data_from_sessions(sessions, user):
    """ Generate the data for a set of selected sessions """

    # List of inventories to exclude
    excludes = []
    if (not user.is_staff):
        for inventory_cls in numeric_inventory_cls_list:
            count = Submission.objects.filter(inventory_id=inventory_cls.inventory_id).count()
            if (count < MINIMUM_SUBMISSIONS):
                excludes.append(inventory_cls.inventory_id)

    # Get all metrics belonging to users
    # registered for each session in sessions.
    # If a session is in the excludes list it is ignored
    # Exclude Via. It is processed separately for simplicity.
    metrics = Metric.objects.filter(
        submission__user__leaduserinfo__session__in=sessions
    ).exclude(
        submission__inventory_id=Via.inventory_id
    ).exclude(
        submission__inventory_id__in=excludes
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

    # Get all via Submissions in selected sessions.
    submissions = Submission.objects.filter(
        inventory_id=Via.inventory_id,
        user__leaduserinfo__session__in=sessions
    )

    if (len(submissions) >= MINIMUM_SUBMISSIONS or user.is_staff):
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
        if (len(via_data.items()) > 0):
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

    if (len(data_list) == 0):
        raise LookupError(NO_DATA)

    return data_list
