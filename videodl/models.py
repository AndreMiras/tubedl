import urllib
from django.db import models
from uuidfield import UUIDField


class DownloadLink(models.Model):
    """
    Share a download.
    """
    uuid = UUIDField(auto=True)
    title = models.CharField(max_length=255, blank=True, default="")
    url = models.URLField(max_length=255)
    created = models.DateTimeField(auto_now=True)
    last_download = models.DateTimeField(auto_now_add=True) # whenever views is incremented
    views = models.PositiveIntegerField(default=0)
    video_path = models.CharField(max_length=255, blank=True, default="")
    audio_path = models.CharField(max_length=255, blank=True, default="")

    def __unicode__(self):
        return "%s" % (self.url)

    def get_file_paths(self):
        file_paths = [self.video_path, self.audio_path]
        return file_paths

    def get_url_friendly_title(self):
        title_sanitized = urllib.quote(self.title.encode('utf8'))
        return title_sanitized

    def get_file_path(self, audio=False):
        if audio:
            return self.audio_path
        return self.video_path

    def set_file_path(self, file_path, audio=False):
        if audio:
            self.audio_path = file_path
        else:
            self.video_path = file_path
