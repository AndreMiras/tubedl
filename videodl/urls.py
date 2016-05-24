from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'videodl.views',
    # url(r'^$', 'download_form', name='download_form'),
    url(r'^download_form/$', 'download_form', name='download_form'),
    url(r'^video_info/(?P<download_link_uuid>[\w]+)/$',
        'video_info', name='video_info'),
    url(r'^prepare_download_redirect/(?P<download_link_uuid>[\w]+)/$',
        'prepare_download_redirect', name='prepare_download_redirect'),
    url(r'^serve_video_download/(?P<download_link_uuid>[\w]+)/$',
        'serve_video_download', name='serve_video_download'),
    url(r'^serve_audio_download/(?P<download_link_uuid>[\w]+)/$',
        'serve_audio_download', name='serve_audio_download'),
    url(r'^supported_sites/$', 'supported_sites', name='supported_sites'),
)
