from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.views.generic import View
import Stations.models as models
from datetime import *
from time import mktime

def sensorView(request, station='', sensor=''):
    station_obj = models.Station.objects.get(name=station)
    sensor_obj = models.Sensor.objects.get(slug=sensor, station=station_obj)
    last2days = datetime.now() - timedelta(2)
    data = models.SensorData.objects.filter(sensor=sensor_obj, timestamp__gte=last2days)
    datastr = ''
    for record in data:
        ts = record.timestamp.timestamp()*1000 #highcharts uses unix timestamp in milliseconds
        datastr = datastr + "[{},{}],".format(int(ts), record.val)
    return render(request, "sensor.html", {'data':datastr})

def homepageView(request):
    return render_to_response("index.html")
