from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseBadRequest
import Stations.models as models
import Stations.highchart as highchart
from datetime import datetime, timedelta
import json


def celcius2fahrenheit(c):
    return (c*9.0/5.0)+32


def stationListView(request):
    """Get a list of stations"""
    stations = []
    for station_obj in models.Station.objects.all():
        station = {}
        station['name'] = station_obj.slug

        sensors = [sensor_obj.slug for sensor_obj in
                   models.Sensor.objects.filter(station=station_obj)]

        station['sensors'] = sensors
        stations.append(station)

    JSONstr = json.dumps(stations)
    return HttpResponse(JSONstr, content_type="application/json")


def stationTree(request):
    node_id = request.GET.get('id')
    if node_id == '#':
        root_children = []
        for station in models.Station.objects.all():
            child = {}
            child['text'] = station.name
            child['state'] = {'opened': True}

            #get types
            
            child['children'] = [sensor.get_sensor_type_display() for sensor \
                                 in models.Sensor.objects.\
                                 distinct('sensor_type')]

            root_children.append(child)

        nodes = {'children': root_children, 'id': node_id}

    return HttpResponse(json.dumps(nodes), content_type="application/json")


def defaultSensorView(request, station):
    """Get a list of default sensors shown on front page of station view"""
    station = station.lower()
    sensors = []

    sensor_objs = models.Sensor.objects.filter(station=station,
                                               frontPage=True)
    for sensor in sensor_objs:
        sensors.append(sensor.slug)

    return HttpResponse(json.dumps(sensors), content_type="application/json")


def highchartView(request, station, sensor):
    fmt = '%m-%d-%Y'
    station = station.lower()
    sensor = sensor.lower()

    #get station object
    station_obj = None
    try:
        station_obj = models.Station.objects.get(slug=station)
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

    #generate start end dates from incoming GET string paramiters
    try:
        start = request.GET.get('start', None)
        start = datetime.strptime(start, fmt)
    except:
        start = None
    #only evalueate end if start is set (not None)
    if start is not None:
        try:
            end = request.GET.get('end', None)
            end = datetime.strptime(end, fmt)
        except:
            end = None
    else:
        end = None

    JSONstr = highchart.optionsFromObj(sen_obj, start=start, end=end)

    return HttpResponse(JSONstr, content_type="application/json")


def stationView(request, station=''):
    station = station.lower()
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
        station_obj = models.Station.objects.get(slug=station)

    #if station is not found then return default station page
    if station_obj is None:
        return stationView(request)

    #get default sensors to show on initial station page
    curSensors = models.Sensor.objects.filter(station=station_obj,
                                              frontPage=True)

    #if no sensor matches list of sensor names
    #then return default station page
    if len(curSensors) == 0:
        return stationView(request)

    sensor_list = models.Sensor.objects.filter(station=station_obj,
                                               frontPage=True)
    #convert from a list of objects to a JSON array
    sensor_list = [sensor.slug for sensor in sensor_list]
    sensor_list = json.dumps(sensor_list)

    return render(request, "station.html",
                  {'stations': station_obj_all,
                   'selStation': station_obj,
                   'default_sensor_list': sensor_list})


def homepageView(request):
    station_obj = models.Station.objects.get(name='Windfarm')
    tmp_sensor_obj = models.Sensor.objects.get(name='Tmp_110S_5ft',
                                               station=station_obj)

    last2days = datetime.now() - timedelta(2)
    tmp_data = highchart.dataSince(tmp_sensor_obj, last2days)
    tmp_data_str = highchart.sensorData2HighchartsData(tmp_data,
                                                       celcius2fahrenheit)
    return render(request, "index.html",
                  {'asof': '3:30 PM', 'curtemp': '80',
                   'tempdata': tmp_data_str})
