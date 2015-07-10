from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # /admin
    url(r'^(?i)admin/', include(admin.site.urls), name='admin-view'),

    # /
    url(r'^$', 'Weather.views.homepageView', name='homepage-view'),

    # /stations/
    url(r'^(?i)stations/$', 'Stations.views.stationView', name='station-view'),

    # /stations/?
    url(r'^(?i)stations/(?P<station>.+)/$', 'Stations.views.stationView',
        name='station-view-spec'),

    # /radar
    url(r'^(?i)radar/$', 'Weather.views.radarView',
        name='radar-view'),

    # /forecast
    url(r'^(?i)forecast/$', 'Weather.views.forecastView',
        name='forecast-view'),

    # /station-list/?
    url(r'^(?i)station-list/$', 'Stations.views.stationListView',
        name='station-list'),

    # /graph/?
    url(r'^(?i)graph/(?P<station>.+)/(?P<sensor>.+)/$',
        'Stations.views.highchartView', name='graph-view'),

    # /station-info
    url(r'^(?i)station-info/(?P<station>.*)?$', 'Stations.views.stationInfo',
        name='get-station-info-view'),

    # /station-tree
    url(r'^(?i)station-tree/$','Stations.views.stationTree', name='station-tree'),

    # /download
    url(r'^(?i)download/$', 'Stations.views.downloadView', name='download-view'),

    # /login and all related account reset etc
    url(r'^', include('django.contrib.auth.urls')),

    # /create
    url(r'^(?i)create_account/$', 'Stations.views.createAccountView', name='create_account'),
)
