from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^(?i)admin/', include(admin.site.urls), name='admin-view'),
    url(r'^(?i)$', 'Stations.views.homepageView', name='homepage-view'),
    url(r'^(?i)stations/$', 'Stations.views.stationView', name='station-view'),
    url(r'^(?i)stations/(?P<station>.+)/$', 'Stations.views.stationView',
        name='station-view-spec'),
    url(r'^(?i)station-list/$', 'Stations.views.stationListView',
        name='station-list'),
    url(r'^(?i)station-front/(?P<station>.+)/$',
        'Stations.views.defaultSensorView',
        name='station-front-list'),
    url(r'^(?i)graph/(?P<station>.+)/(?P<sensor>.+)/$',
        'Stations.views.highchartView', name='graph-view'),
)
