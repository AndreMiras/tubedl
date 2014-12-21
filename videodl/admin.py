from django.contrib import admin
from videodl.models import DownloadLink

class DownloadLinkAdmin(admin.ModelAdmin):
    list_display = ("url", "views")
    fields = ("url", "uuid", "created", "views")
    readonly_fields = ("uuid", "created")
    search_fields = ("uuid", "url")

admin.site.register(DownloadLink, DownloadLinkAdmin)
