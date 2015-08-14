# Models
from gl_site.models import Metric, Submission, Organization, Session
from django.db.models import Count, Min, Max, Avg, StdDev, Prefetch
from django.contrib.auth.models import User

# Inventories
from gl_site.inventories import inventory_by_id, inventory_cls_list, numeric_inventory_cls_list
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

    # Returned data set
    data = {}

    # SELECT COUNT from all submissions in the requested session
    # for all inventories. GROUP BY inventory_id.
    # Aggregate by count and annotate results
    data['submission_counts'] = Submission.objects.filter(
        user__leaduserinfo__session__in=sessions
    ).exclude(
        metric__isnull=True
    ).values(
        'inventory_id'
    ).annotate(
        count=Count('inventory_id')
    )

    # Process excludes. Inventories with 0 submissions do not show up,
    # but they will be excluded by default as there are no submissions.
    # Admins will see all submissions.
    excludes = []
    if (not user.is_staff):
        for submission in data['submission_counts']:
            if (submission['count'] < MINIMUM_SUBMISSIONS):
                excludes.append(submission['inventory_id'])

    # If all inventories are excluded, or the number of excluded inventories
    # is equal to the number of inventories which have counts.
    if (len(excludes) == len(inventory_cls_list) or len(excludes) == len(data['submission_counts'])):
        raise LookupError(NO_DATA)

    # If the user is staff they have access to extra analysis
    if (user.is_staff):
        # Get all metrics in the provided sessions that are
        # not in the excludes list or VIA.
        # GROUP BY key and submission.inventory_id.
        # Aggregate on Min, Max, Avg (mean), and StdDev.
        # Annotate selected values with aggregation results.
        data['metrics_analysis'] = Metric.objects.filter(
            submission__user__leaduserinfo__session__in=sessions
        ).exclude(
            submission__inventory_id=Via.inventory_id
        ).exclude(
            submission__inventory_id__in=excludes
        ).values(
            'key', 'submission__inventory_id'
        ).annotate(
            min=Min('value'),
            max=Max('value'),
            mean=Avg('value'),
            standard_deviation=StdDev('value')
        )

    # Get all users, filtered by users that are in in the
    # selected sessions. Prefetch all submissions by
    # user.submission_set as the reverse many to one foreign
    # key relationship held by Submission. Prefetch all metrics
    # by submission_set.metric_set as the reverse many to one
    # foreign key relationship held by Metric. Select organization
    # and session to pre cache values. Order by organization and
    # then by session
    metrics = Prefetch('metric_set',
        to_attr='metrics',
        queryset=Metric.objects.all()
    )
    submissions = Prefetch(
        'submission_set',
        to_attr='submissions',
        queryset=Submission.objects.exclude(
            inventory_id__in=excludes
        ).exclude(
            metric__isnull=True
        ).prefetch_related(metrics)
    )
    data['users'] = User.objects.prefetch_related(
        submissions
    ).select_related(
        'leaduserinfo__organization', 'leaduserinfo__session'
    ).filter(
        leaduserinfo__session__in=sessions
    ).order_by(
        'leaduserinfo__organization', 'leaduserinfo__session'
    )

    return data

def format_graph_data(preformatted):
    """ Format data as needed for displaying graphs.
        Expects data to be a dict containing users,
        metric_analysis, and submission_counts as
        returned by generate_data_from_sessions.
    """

    # Returned data set
    data = {inventory.name: {} for inventory in inventory_cls_list}

    # Format the analysis if it exists
    if ('metrics_analysis' in preformatted):
        for analysis in preformatted['metrics_analysis']:
            # Inventory
            inventory = inventory_by_id[analysis['submission__inventory_id']]

            # If not initialized, add the analysis
            if ('analysis' not in data[inventory.name]):
                data[inventory.name]['analysis'] = {}

            # Add the analysis
            key = analysis['key']
            data[inventory.name]['analysis'][key] = [
                {'metric': key, 'type': 'min', 'value': analysis['min']},
                {'metric': key, 'type': 'max', 'value': analysis['max']},
                {'metric': key, 'type': 'mean', 'value': analysis['mean']},
                {'metric': key, 'type': 'standard_deviation', 'value': analysis['standard_deviation']},
            ]

    # Format the submission counts
    for inventory in preformatted['submission_counts']:
        # Inventory
        inventory_name = inventory_by_id[inventory['inventory_id']].name

        # Set the submission count
        data[inventory_name]['submission_count'] = inventory['count']

    # Format the metrics for all users
    metric_id = 0
    for user in preformatted['users']:
        # For all submissions the user has made
        for submission in user.submissions:
            inventory_name = inventory_by_id[submission.inventory_id].name

            # Initialize metrics if it doesn't exist
            if ('metrics' not in data[inventory_name]):
                data[inventory_name]['metrics'] = {}

            # Process VIA
            if (inventory_name == Via.name):
                # Get the signature strengths from the metrics
                metrics = submission.metrics
                strength_list = sorted(metrics, key=lambda metric: metric.value, reverse=True)
                strength_list = strength_list[:Via.n_signature]

                # Process each signature strength
                for strength in strength_list:
                    if (strength.key not in data[inventory_name]['metrics']):
                        data[inventory_name]['metrics'][strength.key] = 0

                    data[inventory_name]['metrics'][strength.key] += 1

            # Non VIA inventories
            else:
                # For each metric in the submission
                for metric in submission.metrics:
                    # If the metric list does not exist
                    if (metric.key not in data[inventory_name]['metrics']):
                        data[inventory_name]['metrics'][metric.key] = []

                    # Append the value to the data set
                    data[inventory_name]['metrics'][metric.key].append({
                        "name": ("Metric-{}".format(metric_id)),
                        "key": metric.key,
                        "value": metric.value
                    })

            metric_id += 1

    # Return an ordered list
    data_list = []
    for key, value in data.items():
        # Only add the metrics if any exist
        if ('metrics' in value):
            inventory = {'inventory': key, 'count': value['submission_count'], 'data': []}

            if (key == Via.name):
                for strength, num_signature in value['metrics'].items():
                    inventory['data'].append({
                        'name': via_inverse[strength], # Via category
                        'key': strength,
                        'value': num_signature
                    })
            else:
                for sublist in value['metrics'].values():
                    inventory['data'] += sublist

            if ('analysis' in value):
                inventory['analysis'] = []

                for analysis in value['analysis'].values():
                    inventory['analysis'].append(analysis)

            data_list.append(inventory)

    data_list = sorted(data_list, key=lambda k: k['inventory'])

    return data_list

def format_file_data(preformatted):
    """ Format data as needed for downloading files.
        Expects data to be a dict containing users,
        metric_analysis, and submission_counts as
        returned by generate_data_from_sessions.
    """

    # Data list to be returned
    data = []

    # Process each user
    for user in preformatted['users']:
        if (user.submissions):
            user_data = {
                'organization': user.leaduserinfo.organization.name,
                'session': user.leaduserinfo.session.name
            }

            # Process all submissions
            for submission in user.submissions:
                inventory_name = inventory_by_id[submission.inventory_id].name
                user_data[inventory_name] = {}

                # Proccess all metrics
                for metric in submission.metrics:
                    user_data[inventory_name][metric.key] = metric.value

            # Append data
            data.append(user_data)

    return data
