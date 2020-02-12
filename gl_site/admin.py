# Import admin for model admin
from django.contrib import admin
from django.urls import reverse
import django.contrib.auth as auth

# Model imports
from django.contrib.auth.models import User
from gl_site.models import Organization, Session
from gl_site.config_models import SiteConfig, DashboardText


admin.site.unregister(User)
@admin.register(User)
class UserAdmin(auth.admin.UserAdmin):
    """
    Prevent anyone from creating a User through the admin site.

    Extends the default auth.admin.UserAdmin. Users should only be
    created through the registration page, excluding the initial admin
    user, which is created using `manage.py createsuperuser`.
    """
    
    def has_add_permission(self, request):
        return False


class InlineSessionAdmin(admin.TabularInline):
    """ Inline class for managing sessions within the organization editor """
    model = Session
    can_delete = False

    # Set fields
    readonly_fields = ('created_by', 'creation_date', 'get_url')
    fields = ('name',) + readonly_fields

    def get_url(self, instance):
        """ Return an absolute url to the session's registration page """
        if instance.uuid != "":
            configs = SiteConfig.objects.all()

            if configs.exists():
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


@admin.register(DashboardText)
class DashboardTextAdmin(admin.ModelAdmin):
    """
    Prevent anyone from creating or deleting a DashboardText object.

    Our migrations create a single DashboardText object, and there
    should always be exactly one.
    """

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
