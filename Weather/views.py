from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.template import RequestContext, loader
import Stations.highchart as highchart
from Weather.models import Forecast as ForecastModel
from Weather.models import WMSRadarOverlay as WMSRadarOverlayModel
from Stations.models import Station as StationModel
from Stations.models import Sensor as SensorModel
from Weather.util import updateForecast
from datetime import timedelta


def celsius2fahrenheit(c):
    return (c*9.0/5.0)+32

def radarView(request):
    WMSOverlays = WMSRadarOverlayModel.objects.filter(active=True)

    template = loader.get_template('radar.html')
    context = RequestContext(request, {'wms_overlays': WMSOverlays})

    response = HttpResponse(template.render(context))

    return response


def forecastView(request):
    # check if NWS forecast data needs updated
    # only update once every 2 hours
    obj = ForecastModel.objects.get(days=7, hours=12, location='Hays, KS')
    if obj.refreshed == None or \
        timezone.now() - obj.refreshed > timedelta(hours=2):

        updateForecast(obj)

    return HttpResponse(obj.json_forecast, content_type="application/json")

def homepageView(request):
    station_obj = StationModel.objects.get(name='Windfarm')
    tmp_sensor_obj = SensorModel.objects.get(name='Tmp_110S_5ft',
                                               station=station_obj)

    last2days = timezone.now() - timedelta(2)
    tmp_data = highchart.dataSince(tmp_sensor_obj, last2days)
    tmp_data_str = highchart.sensorData2HighchartsData(tmp_data,
                                                       celsius2fahrenheit)
    return render(
        request,
        "index.html",
        {
            'tempdata': tmp_data_str
        }
    )
