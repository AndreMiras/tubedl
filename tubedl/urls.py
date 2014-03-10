from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tubedl.views.home', name='home'),
    url(r'^contact/$', 'tubedl.views.contact', name='contact'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^dl/', include('videodl.urls')),
)
