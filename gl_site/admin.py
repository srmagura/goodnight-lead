# Import admin for model admin
from django.contrib import admin

# Model imports
from gl_site.models import Organization, Session, SiteConfig

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
            configs = SiteConfig.objects.all()

            if configs.exists():
                config = configs[0]
                base_url = configs[0].base_url
            else:
                base_url = '[base_url]'

            rel = reverse('register', args=(instance.uuid, ))
            url = "{}{}".format(base_url, rel)
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

    def render_change_form(self, request, context, *args, **kwargs):
        """
        Add one of our own variables to the template's context.

        (This ModelAdmin is rendered using a customized template.)
        """
        context['show_save_url'] = not SiteConfig.objects.all().exists()
        return super().render_change_form(request, context, *args, **kwargs)
