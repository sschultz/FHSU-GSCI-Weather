from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.views.generic import View
import Stations.models as models
from datetime import *
from time import mktime
from dateutil.tz import tzutc

def timestamp(ts):
    "Return POSIX timestamp as float as per Python3"
    _EPOCH = datetime(1970, 1, 1, tzinfo=tzutc())
    if ts.tzinfo is None:
        return mktime((ts.year, ts.month, ts.day,
            ts.hour, ts.minute, ts.second,
            -1, -1, -1)) + self.microsecond / 1e6
    else:
        return (ts - _EPOCH).total_seconds()

def sensorView(request, station='', sensor=''):
    station_obj = models.Station.objects.get(name=station)
    sensor_obj = models.Sensor.objects.get(slug=sensor, station=station_obj)
    last2days = datetime.now() - timedelta(2)
    data = models.SensorData.objects.filter(sensor=sensor_obj, timestamp__gte=last2days)
    datastr = ''
    for record in data:
        ts = timestamp(record.timestamp)*1000 #highcharts uses unix timestamp in milliseconds
        datastr = datastr + "[{},{}],".format(int(ts), record.val)
    return render(request, "sensor.html", {'data':datastr})

def homepageView(request):
    return render_to_response("index.html")
