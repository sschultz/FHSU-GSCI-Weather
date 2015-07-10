from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import Stations.models as models
import Stations.highchart as highchart
from Stations.forms import CreateAccountForm
from datetime import datetime, timedelta
from collections import OrderedDict
from html import escape as html_escape
import json


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
    """Station Info View for station specific Info in JSON format"""
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
    if node_id is None:
        return HttpResponseBadRequest("Bad Request: Must know station")

    elif node_id == '#':
        for station in models.Station.objects.all():
            # for each station create a subfolder for each type of sensor
            children = []
            all_sensors = models.Sensor.objects.filter(station=station).order_by('sensor_type')

            sensor_type_full_name = dict(models.SENSOR_TYPE)
            for sensor in all_sensors:
                # all sensor are children of the root station
                children.append({
                    'id': '.'.join((station.slug, sensor.slug,)),
                    'text': sensor.get_formatted_name(),
                    'children': False
                })

            # stations are roots
            root_children.append({
                'text': station.name,
                'id': station.slug,
                'state': {'opened': True},
                'children': children,
            })
            nodes = {'children': root_children, 'id': node_id}

    else:
        # is a child node
        return HttpResponseBadRequest("Bad Request: No Children Nodes")
    
    return HttpResponse(json.dumps(nodes), content_type="application/json")


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
    #only evaluate end if start is set (not None)
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
            # if ...objects.all() returns None
            # then ...objects.all()[0] will cause an exception
            return HttpResponseNotFound('<h1>Default station not found</h1>')
    else:
        station_obj = models.Station.objects.get(slug=station)

    # if station is not found then return default station page
    if station_obj is None:
        return stationView(request)

    # get default sensors to show on initial station page
    sensor_list = models.Sensor.objects.filter(station=station_obj,
                                              frontPage=True)

    # if no sensor matches list of sensor names
    # then return default station page
    if sensor_list.count() == 0:
        return stationView(request)

    # convert from a list of objects to a JSON array
    sensor_list = [(sensor.station.slug, sensor.slug) for sensor in sensor_list]
    sensor_list = json.dumps(sensor_list)

    return render(request, "station.html",
                  {'stations': station_obj_all,
                   'selStation': station_obj,
                   'default_sensor_list': sensor_list})


@login_required(login_url='/login/')
def downloadView(request):
    return HttpResponse('Logged in!!!')


def createAccountView(request):
    if request.method == 'POST':
        # Handle Post Request
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            # TODO: Create User
            return redirect('download-view')
    else:
        # Create a blank form initially
        form = CreateAccountForm()
    return render(request, 'registration/create.html', {'form': form})
