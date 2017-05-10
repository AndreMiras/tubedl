from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.views.generic.base import RedirectView

admin.autodiscover()
handler500 = 'tubedl.views.custom_500'


urlpatterns = patterns(
    '',
    # some browsers assume favicon.ico is present in the root directory
    url(r'^favicon\.ico$',
        RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)),
    url(r'^$', 'tubedl.views.home', name='home'),
    url(r'^contact/$', 'tubedl.views.contact', name='contact'),
    url(r'^error404/$', 'tubedl.views.error404', name='error404'),
    url(r'^error500/$', 'tubedl.views.error500', name='error500'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^dl/', include('videodl.urls')),
)
