from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('videodl.views',
    # url(r'^$', 'download_form', name='download_form'),
    url(r'^download_form/$', 'download_form', name='download_form'),
    url(r'^video_info/(?P<download_link_uuid>[\w]+)/$', 'video_info', name='video_info'),
    url(r'^download_video/(?P<download_link_uuid>[\w]+)/$', 'download_video', name='download_video'),
    url(r'^supported_sites/$', 'supported_sites', name='supported_sites'),
)
