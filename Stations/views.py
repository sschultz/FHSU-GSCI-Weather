from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.views.generic import View
import Stations.models as models
import json
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


def sensorDataFromObjs(sensor_objs):
    sensors = []
    for sensor in sensor_objs:
        data = dataFromLast2Days(sensor)

        highchart_args = {}
        highchart_args['title'] = {'text':sensor.description}

        xAxis = {'text':"Date/Time"}
        xAxis['type'] = "datetime"

        yAxis = {'text':sensor.sensor_type}

        series = {'name':sensor.name}
        series['data'] = [[d_obj.timestamp.timestamp()*1000,
                d_obj.val] for d_obj in data]

        highchart_args['xAxis']  = xAxis
        highchart_args['yAxis']  = yAxis
        highchart_args['series'] = [series]

        json_str = json.dumps(highchart_args, indent=2)
        sensors.append({'divtagid':sensor.slug, 'JSON':json_str})

    return sensors

def sensorView(request, station='', sensors=[]):
    station_obj_all = models.Station.objects.all()
    station_obj = None
    if station == '':
        try:
            station_obj = models.Station.objects.get(name='Windfarm')
            if station_obj == None:
                station_obj = models.Station.objects.all()[0]
                if station_obj == None:
                    return HttpResponseNotFound('<h1>Default station not found</h1>')
        except:
            return HttpResponseNotFound('<h1>Default station not found</h1>')
    else:
        station_obj = models.Station.objects.get(name=station)
    
    #if station is not found then return default station page
    if station_obj == None:
        return sensorView(request)

    sensor_objs = models.Sensor.objects.filter(station=station_obj)
    curSenors = []
    if len(sensors) == 0:
        curSensors = models.Sensor.objects.filter(station=station_obj, frontPage=True)
    else:
        for sensor_name in sensors:
            curSensors.append(models.Sensor.objects.get(station=station_obj, name=sensor_name))

    #if no sensor matches list of sensor names then return default station page
    if len(curSensors) == 0:
        return sensorView(request)

    sensor_data = sensorDataFromObjs(curSensors)
    return render(request, "sensor.html", {'stations':station_obj_all, 'sensors':sensor_data})

def homepageView(request):
    station_obj = models.Station.objects.get(name='Windfarm')
    tmp_sensor_obj = models.Sensor.objects.get(name='Tmp_110S_5ft',
            station=station_obj)

    tmp_data = dataFromLast2Days(tmp_sensor_obj)
    tmp_data_str = sensorData2HighchartsData(tmp_data, celcius2fahrenheit)
    return render(request, "index.html", {'asof':'3:30 PM', 'curtemp':'80', 'tempdata':tmp_data_str})
