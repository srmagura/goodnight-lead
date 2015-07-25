from django import forms

from gl_site.models import Organization, Session

class statistics_request_form(forms.Form):
    """ Form used for requesting statistics from the statistics page """

    organization = forms.ModelChoiceField(queryset=None)

    session = forms.ModelChoiceField(queryset=None, required=False)

    def __init__(self, organizations, sessions, *args, **kwargs):
        super(statistics_request_form, self).__init__(*args, **kwargs)

        # Set field query sets
        self.fields['organization'].queryset = organizations
        self.fields['session'].queryset = sessions
