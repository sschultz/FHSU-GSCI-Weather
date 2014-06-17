from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'FHSU_GSCI_Weather.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'Stations.views.homepageView'),
    url(r'^Stations/(?P<station>.+)/(?P<sensor>.+)/$', 'Stations.views.sensorView'),
)
