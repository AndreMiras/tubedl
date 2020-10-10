import os
from unittest import skipIf

from django.http import JsonResponse
from django.test import TestCase
from django.urls import reverse

from videodl.models import DownloadLink


def run_in_ci():
    """Returns True if running in the CI."""
    return "CI" in os.environ


class TestVideoDl(TestCase):
    def test_regression_isabelle_facebook_video(self):
        """
        This is a regression test a video that returned a Download error
        during info extraction.
        The error was:
        DownloadError: ERROR: requested format not available
        The video was:
        https://www.facebook.com/isabelleparemma/videos/180500918954548/
        """
        video_url = (
            "" + "https://www.facebook.com" + "/isabelleparemma/videos/180500918954548/"
        )
        download_form_url = reverse("download_form")
        response = self.client.post(download_form_url, {"url": video_url}, follow=True)
        # verifies the status_code is OK
        assert response.status_code == 200
        # verifies the info e.g. title could actually be extracted
        assert b"Mon premier combat" in response.content

    def test_url_not_supported(self):
        """
        Not supported URLs shoudln't crash the application,
        but display an error message.
        """
        video_url = "" + "http://foobar.com" + "/video123/"
        download_form_url = reverse("download_form")
        response = self.client.post(download_form_url, {"url": video_url}, follow=True)
        # verifies the status_code is OK
        assert response.status_code == 200
        # verifies the form error message
        assert b"URL not supported." in response.content

    @skipIf(
        run_in_ci(), "TravisCI is sometimes blocked from Youtube on too many requests"
    )
    def test_incomplete_youtube_id(self):
        """
        Video with a wrong ID shoudln't crash the application,
        but display an error message.
        """
        video_url = "" + "https://www.youtube.com" + "/watch?v=foobar"
        download_form_url = reverse("download_form")
        response = self.client.post(download_form_url, {"url": video_url}, follow=True)
        # verifies the status_code is OK
        assert response.status_code == 200
        # verifies the form error message
        assert b"Incomplete YouTube ID" in response.content

    @skipIf(
        run_in_ci(), "TravisCI is sometimes blocked from Youtube on too many requests"
    )
    def test_url_not_found(self):
        """
        Video not found shoudln't crash the application,
        but display an error message.
        """
        video_url = "" + "https://www.youtube.com" + "/watch?v=foofubarfoo"
        download_form_url = reverse("download_form")
        response = self.client.post(download_form_url, {"url": video_url}, follow=True)
        # verifies the status_code is OK
        assert response.status_code == 200
        # verifies the form error message
        assert b"Unable to extract video data" in response.content

    @skipIf(
        run_in_ci(), "TravisCI is sometimes blocked from Youtube on too many requests"
    )
    def test_download_process(self):
        """
        Go through the whole downloading process with a short video.
        """
        video_url = "" + "https://www.youtube.com" + "/watch?v=t3NZusaDt1M"
        # no DownloadLink object for this URL in the database before starting
        assert DownloadLink.objects.filter(url=video_url).exists() is False
        download_form_url = reverse("download_form")
        response = self.client.post(download_form_url, {"url": video_url}, follow=True)
        # verifies the status_code is OK
        assert response.status_code == 200
        # verifies the title could actually be extracted
        assert b"Double Exposure Effect  - Short Video" in response.content
        # the DownloadLink object should have been created
        download_link = DownloadLink.objects.get(url=video_url)
        # use the UUID to go to the prepare_download_redirect page
        prepare_download_redirect_url = reverse(
            "prepare_download_redirect",
            kwargs={"download_link_uuid": download_link.uuid.hex},
        )
        response = self.client.post(
            prepare_download_redirect_url, {"audio_only": False}
        )
        # verifies the status_code is OK
        assert response.status_code == 200
        assert isinstance(response, JsonResponse)
        # the JSON response should give the download_redirect_url
        assert b"download_redirect_url" in response.content
        assert download_link.uuid.hex in response.content.decode("utf-8")
        # accesses serve_video_download url
        serve_video_download_url = reverse(
            "serve_video_download",
            kwargs={"download_link_uuid": download_link.uuid.hex},
        )
        response = self.client.get(serve_video_download_url)
        # verifies the status_code is OK
        # if not and the /tmp/ directory contains two files with different
        # formats e.g. t3NZusaDt1M.f140.m4a and t3NZusaDt1M.f137.mp4
        # it's because you need ffmpeg or avconv for it to be merged into
        # a single file
        assert response.status_code == 200
        # verifies there is an attachment
        assert "attachment; filename=" in response["Content-Disposition"]
        assert ".mp4" in response["Content-Disposition"]
        # checking the video size
        # it seems the size may vary slightly from one libav to the other
        # so we round it
        size_oct = len(response.content)
        size_meg = round(float(size_oct) / pow(10, 6), 2)
        assert size_meg == 9.87
