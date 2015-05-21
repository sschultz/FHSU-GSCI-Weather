# suds-jurko library required
from suds.client import Client as SOAPClient
from Weather.models import Forecast
import xml.etree.ElementTree as ET
from datetime import datetime
import django.core.exceptions as django_ex
import json

HaysLat, HaysLon = '38.885425', '-99.317830'
SOAP_URL = r'http://graphical.weather.gov/xml/DWMLgen/wsdl/ndfdXML.wsdl'
layoutKey = r'k-p12h-n14-3'
forecastDBname = '12 Hour 7 Day'

def updateHaysForecast():
    # extract NWS data from SOAP server
    client = SOAPClient(SOAP_URL)

    # definition:
    # NDFDgenByDay(lat, lon, startDate, numDays, Units, format)
    results = client.service.NDFDgenByDay(
        HaysLat,  # lat
        HaysLon,  # lon
        '',  # startDate (unnecessary for full 7 day forecasting)
        '7',  # numDays
        'e',  # Unit (either 'e' for english standard or 'm' for metric)
        '12 hourly'  # format, either '12 hourly' or '24 hourly (e.i. 6:00 AM - 6:00 AM)'
    )

    # use ElementTree to parse returned xml
    root = ET.fromstring(results)

    assert isinstance(root, ET.Element)

    time_layout = root.find("./data/time-layout/[layout-key='%s']" % layoutKey)
    assert isinstance(time_layout, list)

    periods = [period.get('period-name') for period in time_layout.findall('./start-valid-time')]

    data = {
        'periods': periods
    }

    try:
        obj = Forecast.objects.get(type=forecastDBname)
        obj.update(refreshed=datetime.now(), json_str=json.dumps(data))
        obj.full_clean()
        obj.save()

    except django_ex.ObjectDoesNotExist:
        obj = Forecast.objects.create(type=forecastDBname, refreshed=datetime.now(), json_str=json.dumps(data))
        obj.full_clean()
        obj.save()