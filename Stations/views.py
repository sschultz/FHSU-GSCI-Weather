from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseBadRequest
import Stations.models as models
import Stations.highchart as highchart
from datetime import datetime, timedelta
from collections import OrderedDict
import json


def celcius2fahrenheit(c):
    return (c*9.0/5.0)+32


def getDefaultStationObj():
    #first try to get windfarm
    station_obj = models.Station.objects.get(name='Windfarm')
    if station_obj is None:
        #no default station found, fall back on first loaded station
        station_obj = models.Station.objects.all()[0]
    return station_obj


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


def stationInfo(request, station=''):
    try:
        if station == '':
            stationObj = getDefaultStationObj()
        else:
            station = station.lower()
            stationObj = models.Station.objects.get(slug=station)

        assert isinstance(stationObj, models.Station)
    except:
        return HttpResponseNotFound('<h1>Unable to find station</h1>')

    details = OrderedDict((
        ('name', stationObj.name),
        ('slug', stationObj.slug),
        ('description', stationObj.description),
        ('active', stationObj.active),
    ))

    defaultSensors = lambda obj: models.Sensor.objects.filter(station=obj, frontPage=True)
    sensors = lambda obj: models.Sensor.objects.filter(station=obj)

    #build a list of all sensors on this station
    details['default_sensors'] = [sen.slug for sen in defaultSensors(stationObj)]
    details['sensors'] = [sen.slug for sen in sensors(stationObj)]

    return HttpResponse(json.dumps(details, indent=True), content_type="application/json")

def stationTree(request):
    node_id = request.GET.get('id')
    #if root node (build tree base/trunk)
    root_children = []
    if node_id == '#':
        for station in models.Station.objects.all():
            #create a folder for each station
            child = {}
            child['text'] = station.name
            child['state'] = {'opened': True}
            
            #for each station create a subfolder for each type of sensor
            children = []
            all_sensors = models.Sensor.objects.filter(station=station)
            all_sensors_distinct_types = [sensor.sensor_type for sensor in
                            all_sensors.distinct('sensor_type')]

            sensor_type_full_name = dict(models.SENSOR_TYPE)
            for sensor_type in all_sensors_distinct_types:
                sensor_type_child = {}
                
                sensor_type_child['id'] = station.name + '::' + sensor_type
                sensor_type_child['text'] = sensor_type_full_name[sensor_type]
                sensor_type_child['children'] = True
                sensor_type_child['state'] = ['closed']
                
                children.append(sensor_type_child)

            child['children'] = children
            root_children.append(child)
            nodes = {'children': root_children, 'id': node_id}
    else:
        #is a child node
        station_name, sensor_type = node_id.split('::')
        station = models.Station.objects.get(name=station_name)
        sensors = models.Sensor.objects.filter(station=station,
                                               sensor_type=sensor_type)
        #for each sensor
        for sensor in sensors:
            child = {}
            child['id'] = station.name + ".." +sensor.name
            child['text'] = sensor.name
            root_children.append(child)
        nodes = root_children
    
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

    if station == '':
        try:
            station_obj = getDefaultStationObj()
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
