# Forms
from django import forms

# Models
from gl_site.models import Session

# Utils
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.html import format_html

class SessionWidget(forms.widgets.Select):
    """ Session Widget to allow custom rendering of select options """

    def render_option(self, selected_choices, option_value, option_label):
        """ Render options with organization attribute for UI utils.
            Code based on Django source for forms.widget.Select.
            Overrides forms.widget.Select render_option.
        """

        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''

        try:
            if (option_value == ''):
                option_value = 0
            org = Session.objects.get(id=option_value).organization.id
        except Session.DoesNotExist:
            org = ''
            option_value=''

        return format_html('<option organization="{}" value="{}"{}>{}</option>',
                           org,
                           option_value,
                           selected_html,
                           force_text(option_label))

class statistics_request_form(forms.Form):
    """ Form used for requesting statistics from the statistics page """

    # The organization being requested
    organization = forms.ModelChoiceField(queryset=None, required=False)

    # The session being requested
    session = forms.ModelChoiceField(queryset=None, required=False, widget=SessionWidget)

    def __init__(self, organizations, sessions, *args, **kwargs):
        """ Override init to set field querysets manually """

        super(statistics_request_form, self).__init__(*args, **kwargs)

        # Set field query sets
        self.fields['organization'].queryset = organizations
        self.fields['session'].queryset = sessions

        #Set custom class and empty field on all widgets
        for field in self.fields.values():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs.update({'class':'form-control'})

            if hasattr(field, 'queryset'):
                if field.queryset.count() == 1:
                    field.empty_label = None
                else:
                    field.empty_label = "All"

class statistics_download_form(statistics_request_form):
    """ Form for performing a data download """

    # Download choices
    choices = (
        ('application/xlsx', 'Excel spreadsheet (for typical use)'),
        ('application/json', 'JSON (for technical users)')
    )
    file_type = forms.ChoiceField(choices=choices)

    def __init__(self, *args, **kwargs):
        """ Set ModelChoiceFields to hidden inputs """

        super(statistics_download_form, self).__init__(*args, **kwargs)

        self.fields['organization'].widget = forms.HiddenInput()
        self.fields['session'].widget = forms.HiddenInput()
