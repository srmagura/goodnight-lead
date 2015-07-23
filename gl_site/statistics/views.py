from django.shortcuts import render
from gl_site.custom_auth import login_required

# @login_required
def view_statistics(request):
    return render(request, 'statistics/statistics.html', {})
