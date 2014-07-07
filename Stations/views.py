from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
import Stations.models as models
import json
from datetime import datetime, timedelta


def celcius2fahrenheit(c):
    return (c*9.0/5.0)+32


def dataFromLast2Days(sensor):
    last2days = datetime.now() - timedelta(2)
    return models.SensorData.objects.filter(sensor=sensor,
                                            timestamp__gte=last2days)


def sensorData2HighchartsData(data_rec, converter=None):
    datastr = ''
    for record in data_rec:
         #highcharts uses unix timestamp in milliseconds
        ts = record.timestamp.timestamp()*1000
        if converter is None:
            val = record.val
        else:
            val = converter(record.val)
        datastr = datastr + "[{},{}],".format(int(ts), val)
    return datastr


def JSONhighchartFromObjs(sensor_objs):
    sensors = []
    for sensor in sensor_objs:
        data = dataFromLast2Days(sensor)

        highchart_args = {}
        highchart_args['title'] = {'text': sensor.description}

        xAxis = {'text': "Date/Time"}
        xAxis['type'] = "datetime"

        yAxis = {'text': sensor.sensor_type}

        series = {'name': sensor.name}
        series['data'] = [[d_obj.timestamp.timestamp()*1000,
                           d_obj.val] for d_obj in data]

        highchart_args['xAxis'] = xAxis
        highchart_args['yAxis'] = yAxis
        highchart_args['series'] = [series]

        json_str = json.dumps(highchart_args, indent=2)
        sensors.append({'divtagid': sensor.slug, 'JSON': json_str})

    return sensors


def highchartView(request, station='', sensor=''):
    if station == '':
        return HttpResponseNotFound('<h1>Unable to find station</h1>')
    if sensor == '':
        return HttpResponseNotFound('<h1>Unable to find sensor on ' +
                                    station + '</h1>')

    #get station object
    station_obj = None
    try:
        station_obj = models.Station.objects.get(name=station)
    except:
        return HttpResponseNotFound('<h1>Unable to find station</h1>')

    if station_obj is None:
        return HttpResponseNotFound('<h1>Unable to find station</h1>')

    #get sensor object
    sen_obj = None
    try:
        sen_obj = models.Sensor.objects.get(station=station_obj, slug=sensor)
    except:
        return HttpResponseNotFound('<h1>Unable to find sensor</h1>')

    JSONstr = JSONhighchartFromObjs(sen_obj)

    return HttpResponse(JSONstr, content_type="text/plain")


def stationView(request, station='', sensors=[]):
    station_obj_all = models.Station.objects.all()
    station_obj = None
    #first try if no station specified then choose a default
    if station == '':
        try:
            station_obj = models.Station.objects.get(name='Windfarm')
            if station_obj is None:
                #no default station found, fall back on first loaded station
                station_obj = models.Station.objects.all()[0]
                if station_obj is None:
                    return HttpResponseNotFound('<h1>Default station not '
                                                'found</h1>')
        except:
            #if ...objects.all() returns None
            #then ...objects.all()[0] will cause an exception
            return HttpResponseNotFound('<h1>Default station not found</h1>')
    else:
        station_obj = models.Station.objects.get(name=station)

    #if station is not found then return default station page
    if station_obj is None:
        return stationView(request)

    #get all sensors on this station
    sensor_objs = models.Sensor.objects.filter(station=station_obj)

    #curSensors represents the sensors to be displayed on the page with graphs
    curSenors = []
    #sensors is a list of sensor names to be displayed
    if len(sensors) == 0:
        #no sensors selected, find default sensors with frontPage set to True
        curSensors = models.Sensor.objects.filter(station=station_obj,
                                                  frontPage=True)
    else:
        for sensor_name in sensors:
            curSensors.append(models.Sensor.objects.get(station=station_obj,
                                                        name=sensor_name))

    #if no sensor matches list of sensor names
    #then return default station page
    if len(curSensors) == 0:
        return stationView(request)

    #Create a list of dictionary items containing JSON code and tag names for
    #each sensors being displayed
    sensor_data = JSONhighchartFromObjs(curSensors)
    return render(request, "station.html",
                  {'stations': station_obj_all, 'sensors': sensor_data})


def homepageView(request):
    station_obj = models.Station.objects.get(name='Windfarm')
    tmp_sensor_obj = models.Sensor.objects.get(name='Tmp_110S_5ft',
                                               station=station_obj)

    tmp_data = dataFromLast2Days(tmp_sensor_obj)
    tmp_data_str = sensorData2HighchartsData(tmp_data, celcius2fahrenheit)
    return render(request, "index.html",
                  {'asof': '3:30 PM', 'curtemp': '80',
                   'tempdata': tmp_data_str})
