# Import admin for model admin
from django.contrib import admin

# Model imports
from gl_site.models import Organization, Session

# Reverse and OS used for Session urls
from django.core.urlresolvers import reverse
import os

class InlineSessionAdmin(admin.TabularInline):
    """ Inline class for managing sessions within the organization editor """
    model = Session
    can_delete = False

    # Set fields
    readonly_fields = ('created_by', 'creation_date', 'get_url')
    fields = ('name',) + readonly_fields

    def get_url(self, instance):
        """ Return an absolute url to the session's registration page """
        if instance.uuid is not "":
            # This really shouldn't have to be hardcoded
            # Unfortunately Django seems to have no good method for
            # building an absolute uri without access to the request
            # object and using separate settings files.
            # Use environment variables and set prod as default.
            domain = os.getenv('GOODNIGHT_LEAD_DOMAIN_NAME', 'https://goodnight-lead.herokuapp.com')
            rel = reverse('register', args=(instance.uuid, ))
            url = "{}{}".format(domain, rel)
            return url
        else:
            return ""

    get_url.short_description = "Registration URL"

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """ Organization Model Admin """

    # Which fields to display on the main list
    list_display = ('name', 'creation_date',)

    # Readonly fields
    readonly_fields = ('created_by',)

    # Set the Session inline
    inlines = [InlineSessionAdmin,]

    def save_model(self, request, instance, form, change):
        """ Override save to set created_by """
        instance.created_by = request.user
        instance.save()

    def save_formset(self, request, form, formset, change):
        """ Override save_formset to set session created_by """
        if formset.model == Session:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.created_by = request.user
                instance.save()
            formset.save_m2m()
