from django.conf.urls import url
from django.contrib import admin

from videodl import views

admin.autodiscover()

urlpatterns = [
    url(r'^download_form/$', views.download_form, name='download_form'),
    url(r'^video_info/(?P<download_link_uuid>[\w]+)/$',
        views.video_info, name='video_info'),
    url(r'^prepare_download_redirect/(?P<download_link_uuid>[\w]+)/$',
        views.prepare_download_redirect, name='prepare_download_redirect'),
    url(r'^serve_video_download/(?P<download_link_uuid>[\w]+)/$',
        views.serve_video_download, name='serve_video_download'),
    url(r'^serve_audio_download/(?P<download_link_uuid>[\w]+)/$',
        views.serve_audio_download, name='serve_audio_download'),
    url(r'^supported_sites/$', views.supported_sites, name='supported_sites'),
]
