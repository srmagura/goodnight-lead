# View imports
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from gl_site.custom_auth import login_required

# Forms
from gl_site.statistics.statistics_form import  statistics_request_form, statistics_download_form

# Data
from .data_generation import format_graph_data, format_file_data, generate_data_from_sessions, get_queryset, validate_sessions
from gl_site.statistics import inventory_keys

# IO
from django.core.files.base import ContentFile
from io import BytesIO

# JSON
import json

# Excel
import xlsxwriter

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
    downloads = statistics_download_form(
        querysets['organizations'],
        querysets['sessions'],
        auto_id='id_downloads_%s'
    )
    return render(request, 'statistics/statistics.html', {
        'form': form,
        'downloads': downloads,
        'statistics_active': True,
    })

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

        # Generate and format the data
        data = generate_data_from_sessions(sessions, request.user)
        data = format_graph_data(data)

        # Return the JSON encoded response
        return JsonResponse(data, safe=False)
    except LookupError as e:
        return JsonResponse([str(e)], status=BAD_REQUEST, safe=False)

def download_data(request):
    # Get the querysets accessable by the user
    querysets = get_queryset(request.user)

    # Get the selected downloads
    downloads = statistics_download_form(
        querysets['organizations'],
        querysets['sessions'],
        request.GET,
        auto_id='id_downloads_%s'
    )

    # If it is a valid choice
    if (downloads.is_valid()):
        data = []
        try:
            # Validate sessions
            sessions = validate_sessions(
                downloads.cleaned_data['organization'],
                downloads.cleaned_data['session'],
                request.user
            )

            # Generate the data
            data = generate_data_from_sessions(sessions, request.user)
            data = format_file_data(data)
        except LookupError:
            pass

    else:
        data_file = ContentFile('')

    # Finalize the output
    if (downloads.cleaned_data['file_type'] == 'application/xlsx'):
        # Create an excel workbook wrapped around python byte io.
        # Use in memory to prevent the use of temp files.
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        # Create a worksheet.
        worksheet = workbook.add_worksheet()

        # Set ID, Organization, and Session headers
        worksheet.write('A1', 'User ID')
        worksheet.write('B1', 'Organization')
        worksheet.write('C1', 'Session')

        # Add all user IDs (row number), organization, and session information
        row = 2
        for user in data:
            worksheet.write('A{}'.format(row), row - 1)
            worksheet.write('B{}'.format(row), user['organization'])
            worksheet.write('C{}'.format(row), user['session'])
            row += 1

        # Print inventory data starting at column D
        prefix = ''
        column = ord('D')
        for inventory in inventory_keys:
            # Print all metrics within the inventory
            for key in inventory['keys']:
                # If column is greater than 'Z' move to 'AA'
                if (column > ord('Z')):
                    prefix = 'A'
                    column = ord('A')

                # Write the column header: Inventory - Metric
                worksheet.write(prefix + chr(column) + '1', inventory['name'] + ' - ' + key)

                # Print metric data for each user
                row = 2
                for user in data:
                    inventory_name = inventory['name']
                    # Only print if the user has data for this inventory
                    if (inventory_name in user and key in user[inventory_name]):
                        cell = (prefix + chr(column) + '{}').format(row)
                        worksheet.write(cell, user[inventory['name']][key])

                    # Move on to the next row
                    row += 1

                # Move on to the next column
                column += 1

        # Close the workbook
        workbook.close()

        # Get the output bytes for creating a django file
        output = output.getvalue()

        # Set the appropriate application extension
        extension = '.xlsx'
    else:
        # Generate the JSON output string
        output = json.dumps(data)

        # Set the appropriate application extension
        extension = '.json'

    # Generate the data file
    data_file = ContentFile(output)

    # Create the response containing the file
    response = HttpResponse(
        data_file,
        content_type=downloads.cleaned_data['file_type']
    )
    response['Content-Disposition'] = 'attachment; filename=statistics{}'.format(extension)
    return response
