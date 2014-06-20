from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.views.generic import View
import Stations.models as models
from datetime import *
from time import mktime

def celcius2fahrenheit(c):
    return (c*9.0/5.0)+32

def dataFromLast2Days(sensor):
    last2days = datetime.now() - timedelta(2)
    return models.SensorData.objects.filter(sensor=sensor, timestamp__gte=last2days)

def sensorData2HighchartsData(data_rec, converter=None):
    datastr = ''
    for record in data_rec:
        ts = record.timestamp.timestamp()*1000 #highcharts uses unix timestamp in milliseconds
        if converter == None:
            val = record.val
        else:
            val = converter(record.val)
        datastr = datastr + "[{},{}],".format(int(ts), val)
    return datastr

def sensorView(request, station='', sensor=''):
    station_obj = models.Station.objects.get(name=station)
    sensor_obj = models.Sensor.objects.get(slug=sensor, station=station_obj)
    data = dataFromLast2Days(sensor_obj)
    datastr = sensorData2HighchartsData(data)
    return render(request, "sensor.html", {'data':datastr})

def homepageView(request):
    station_obj = models.Station.objects.get(name='Windfarm')
    tmp_sensor_obj = models.Sensor.objects.get(name='Tmp_110S_5ft',
            station=station_obj)

    tmp_data = dataFromLast2Days(tmp_sensor_obj)
    tmp_data_str = sensorData2HighchartsData(tmp_data, celcius2fahrenheit)
    return render(request, "index.html", {'asof':'3:30 PM', 'curtemp':'80', 'tempdata':tmp_data_str})
