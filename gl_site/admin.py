# Import admin for model admin
from django.contrib import admin

# Model imports
from gl_site.models import Organization

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass
