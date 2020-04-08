import uuid
from urllib.parse import quote

from django.db import models


class DownloadLink(models.Model):
    """Share a download."""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, default="")
    url = models.URLField(max_length=255)
    created = models.DateTimeField(auto_now=True)
    # whenever views is incremented
    last_download = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    video_path = models.CharField(max_length=255, blank=True, default="")
    audio_path = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.url

    def get_file_paths(self):
        file_paths = [self.video_path, self.audio_path]
        return file_paths

    def get_url_friendly_title(self):
        title_sanitized = quote(self.title.encode("utf8"))
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
