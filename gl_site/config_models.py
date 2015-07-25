"""
Models that store site configuration and content.
"""
from django.db import models
from ckeditor.fields import RichTextField

class SiteConfig(models.Model):
    """
    Configuration variables for gl_site.

    There should only ever be one instance of this model.
    """

    base_url = models.CharField(max_length=200)


class DashboardText(models.Model):
    """
    Stores text that is displayed on the dashboard.

    This model can be edited through the admin site. There should only
    ever be one instance of this model.
    """

    inventory_desc = models.TextField()
    mental_health_warning = models.TextField()
    about_panel_title = models.CharField(max_length=128)
    about_panel_contents = RichTextField(help_text=
        'Note: uploading images to the server is not currently supported. '
        'If you want to insert an image that is hosted elsewhere on the web, '
        'you can do so by copying its URL into image insert dialog.'
    )

    def __str__(self):
        return 'DashboardText object'

    class Meta:
        verbose_name = 'Dashboard text'
        verbose_name_plural = 'Dashboard text'
