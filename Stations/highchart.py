import json
import Stations.models as models
#from django.db.models import Avg
from datetime import datetime, timedelta


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


def dataSince(sensor, since):
    return models.SensorData.objects.filter(sensor=sensor,
                                            timestamp__gte=since)


def optionsFromObj(sensor_obj, start=None, end=None, maxpoints=500):
    """Creates a JSON string to configure a highchart object"""
    if start is None:
        last2days = datetime.now() - timedelta(2)
        data = dataSince(sensor_obj, last2days)
    elif end is None:
        data = dataSince(sensor_obj, start)
    else:
        data = models.SensorData.objects.filter(
            sensor=sensor_obj,
            timestamp__range=(start, end+timedelta(1))
        )

#    if data.count() > maxpoints:
        #partition data to reduce number of points
#        data = data.annotate(val_avg=Avg('val')).values('timestamp__range')

    highchart_args = {}
    highchart_args['title'] = {'text': sensor_obj.description}

    xAxis = {'text': "Date/Time"}
    xAxis['type'] = "datetime"

    yAxis = {'text': sensor_obj.sensor_type}

    series = {'name': sensor_obj.name}
    series['data'] = [[d_obj.timestamp.timestamp()*1000,
                       d_obj.val] for d_obj in data]

    highchart_args['xAxis'] = xAxis
    highchart_args['yAxis'] = yAxis
    highchart_args['series'] = [series]

    json_str = json.dumps(highchart_args, indent=2)

    return json_str
