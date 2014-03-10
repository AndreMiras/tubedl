from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('videodl.views',
    # url(r'^$', 'download_form', name='download_form'),
    url(r'^download_form/$', 'download_form', name='download_form'),
)
