from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()
handler500 = 'tubedl.views.custom_500'


urlpatterns = patterns(
    '',
    url(r'^$', 'tubedl.views.home', name='home'),
    url(r'^contact/$', 'tubedl.views.contact', name='contact'),
    url(r'^error404/$', 'tubedl.views.error404', name='error404'),
    url(r'^error500/$', 'tubedl.views.error500', name='error500'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^dl/', include('videodl.urls')),
)
