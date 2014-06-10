from django.conf.urls import patterns, include, url
from Stations.views import SensorView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'FHSU_GSCI_Weather.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'Stations.views.homepage'),
    url(r'^Stations/.*', SensorView.as_view()),
)
