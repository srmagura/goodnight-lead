from django.test import TestCase

from gl_site.models import SiteConfig

class TestBaseURL(TestCase):

    def test_set_base_url(self):
        """
        Verify that the set_base_url view creates the SiteConfig model.
        Visit set_base_url again to check that the SiteConfig is updated
        properly if it already exists.
        """
        for host_name in ('testserver', 'hoohahserver'):
            response = self.client.get('/set_base_url', HTTP_HOST=host_name)
            self.assertTemplateUsed(response, 'set_base_url.html')

            query = SiteConfig.objects.all()
            self.assertTrue(len(query) == 1)

            site_config = query[0]
            self.assertEqual(site_config.base_url, 'http://' + host_name)
