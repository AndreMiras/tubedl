from django.test import TestCase
from django.core.urlresolvers import reverse


class VideoDlTestCase(TestCase):
    def setUp(self):
        pass

    def test_regression_isabelle_facebook_video(self):
        """
        This is a regression test a video that returned a Download error
        during info extraction.
        The error was:
        DownloadError: ERROR: requested format not available
        The video was:
        https://www.facebook.com/isabelleparemma/videos/180500918954548/
        """
        video_url = '' + \
            'https://www.facebook.com' + \
            '/isabelleparemma/videos/180500918954548/'
        download_form_url = reverse('download_form')
        response = self.client.post(
            download_form_url,
            {'url': video_url},
            follow=True)
        # verifies the status_code is OK
        self.assertEqual(response.status_code, 200)
        # verifies the info e.g. title could actually be extracted
        self.assertTrue('Mon premier combat' in response.content)
