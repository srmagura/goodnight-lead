# Import admin for model admin
from django.contrib import admin

# Model imports
from gl_site.models import Organization, Session

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    # Which fields to display on the main list
    list_display = ('name', 'creation_date')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    exclude = ('uuid',)
    list_display = ('name', 'creation_date', 'uuid')
