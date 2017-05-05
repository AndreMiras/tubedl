from django.test import TestCase
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from videodl.models import DownloadLink


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
        self.assertContains(response, 'Mon premier combat')

    def test_url_not_supported(self):
        """
        Not supported URLs shoudln't crash the application,
        but display an error message.
        """
        video_url = '' + \
            'http://foobar.com' + \
            '/video123/'
        download_form_url = reverse('download_form')
        response = self.client.post(
            download_form_url,
            {'url': video_url},
            follow=True)
        # verifies the status_code is OK
        self.assertEqual(response.status_code, 200)
        # verifies the form error message
        self.assertContains(response, 'URL not supported.')

    def test_incomplete_youtube_id(self):
        """
        Video with a wrong ID shoudln't crash the application,
        but display an error message.
        """
        video_url = '' + \
            'https://www.youtube.com' + \
            '/watch?v=foobar'
        download_form_url = reverse('download_form')
        response = self.client.post(
            download_form_url,
            {'url': video_url},
            follow=True)
        # verifies the status_code is OK
        self.assertEqual(response.status_code, 200)
        # verifies the form error message
        self.assertContains(response, 'Incomplete YouTube ID')

    def test_url_not_found(self):
        """
        Video not found shoudln't crash the application,
        but display an error message.
        """
        video_url = '' + \
            'https://www.youtube.com' + \
            '/watch?v=foofubarfoo'
        download_form_url = reverse('download_form')
        response = self.client.post(
            download_form_url,
            {'url': video_url},
            follow=True)
        # verifies the status_code is OK
        self.assertEqual(response.status_code, 200)
        # verifies the form error message
        self.assertContains(response, 'This video does not exist.')

    def test_download_process(self):
        """
        Go through the whole downloading process with a short video.
        """
        video_url = '' + \
            'https://www.youtube.com' + \
            '/watch?v=t3NZusaDt1M'
        # no DownloadLink object for this URL in the database before starting
        self.assertEqual(
            DownloadLink.objects.filter(url=video_url).count(),
            0)
        download_form_url = reverse('download_form')
        response = self.client.post(
            download_form_url,
            {'url': video_url},
            follow=True)
        # verifies the status_code is OK
        self.assertEqual(response.status_code, 200)
        # verifies the title could actually be extracted
        self.assertContains(response, 'Double Exposure Effect  - Short Video')
        # the DownloadLink object should have been created
        download_link = DownloadLink.objects.get(url=video_url)
        # use the UUID to go to the prepare_download_redirect page
        prepare_download_redirect_url = reverse(
            'prepare_download_redirect',
            kwargs={'download_link_uuid': download_link.uuid.hex})
        response = self.client.post(
            prepare_download_redirect_url,
            {'audio_only': False})
        # verifies the status_code is OK
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response, JsonResponse))
        # the JSON response should give the download_redirect_url
        self.assertContains(response, 'download_redirect_url')
        self.assertContains(response, download_link.uuid.hex)
        # accesses serve_video_download url
        serve_video_download_url = reverse(
            'serve_video_download',
            kwargs={'download_link_uuid': download_link.uuid.hex})
        response = self.client.get(serve_video_download_url)
        # verifies the status_code is OK
        self.assertEqual(response.status_code, 200)
        # verifies there is an attachment
        self.assertTrue(
            'attachment; filename=' in response['Content-Disposition'])
        self.assertTrue('.mp4' in response['Content-Disposition'])
        # checking the video size
        self.assertEqual(len(response.content), 9866796)
