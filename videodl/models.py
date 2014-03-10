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
