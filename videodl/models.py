from django.db import models
from uuidfield import UUIDField


class DownloadLink(models.Model):
    """
    Share a download.
    """
    uuid = UUIDField(auto=True)
    url = models.URLField(max_length=100)
    created = models.DateTimeField(auto_now=True)
    last_download = models.DateTimeField(auto_now_add=True) # whenever views is incremented
    views = models.PositiveIntegerField(default=0)
    video_path = models.CharField(max_length=255, blank=True)
    audio_path = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return "%s" % (self.url)

    def get_file_paths(self):
        file_paths = [self.video_path, self.audio_path]
        return file_paths
