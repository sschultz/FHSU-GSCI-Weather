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


def optionsFromObj(sensor_obj, start=None, end=None,
                   types=('AVG', 'MIN', 'MAX'), maxpoints=500):
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
#        partition data to reduce number of points
#        data = data.annotate(val_avg=Avg('val')).values('timestamp__range')

    highchart_args = {}
    highchart_args['title'] = {'text': sensor_obj.description}

    chart = {'renderTo': "%s..%s" % (sensor_obj.station.slug, sensor_obj.slug)}

    xAxis = {'title': {'text': "Date/Time CST (GMT-6)"}}
    xAxis['type'] = "datetime"

    yAxis = {'title': {'text': sensor_obj.get_sensor_type_display()}}
    lbl = {}
    lbl['format'] = '{value} ' + sensor_obj.data_unit
    yAxis['labels'] = lbl

    tooltip = {'valueSuffix': sensor_obj.data_unit}
    tooltip['valueDecimals'] = 2
    #Create a list of series objects for each requested type of data
    seriesList = []
    ValType = dict(models.VALUE_TYPE)
    for t in types:
        try:
            thisdat = data.filter(val_type=t)
            series = {'name': ValType[t]}
            series['tooltip'] = tooltip
            series['data'] = [
                [d_obj.timestamp.timestamp()*1000,
                 d_obj.val] for d_obj in thisdat]
            seriesList.append(series)
        except models.SensorData.DoesNotExist:
            pass

    highchart_args['chart'] = chart
    highchart_args['xAxis'] = xAxis
    highchart_args['yAxis'] = yAxis
    highchart_args['series'] = seriesList

    json_str = json.dumps(highchart_args, indent=2)

    return json_str
