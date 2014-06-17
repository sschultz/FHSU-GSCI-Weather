from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.views.generic import View
import Stations.models as models
import datetime

def sensorView(request, station='', sensor=''):
    station_obj = models.Station.objects.get(name=station)
    sensor_obj = models.Sensor.objects.get(slug=sensor, station=station_obj)
    last2days = datetime.datetime.now() - timedelta(2)
    data = models.SensorData.objects.filter(sensor=sensor_obj, timestamp__gte=last2days)
    return render(request, "sensor.html", {'data':data})

def homepageView(request):
    return render_to_response("index.html")
