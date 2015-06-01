# suds-jurko library required

from collections import OrderedDict
import xml.etree.ElementTree as ET
from datetime import datetime, time
import logging
from suds.client import Client as SOAPClient

import json

SOAP_URL = r'http://graphical.weather.gov/xml/DWMLgen/wsdl/ndfdXML.wsdl'
layoutKeys = {
    '12hour': r'k-p12h-n14-3',
    'daily': r'k-p24h-n7-1',
    'nightly': r'k-p24h-n7-2'
}

# check if start and end period's midpoint is before 6:00 PM
def isMidday(start, end):
    """get the mid period time only (strip calender date)"""
    mid = datetime.time((end-start)/2 + start)
    return mid < time(18)

def xml2date(s):
    """Convert XML time string to python datetime object"""
    return datetime.strptime(s[:22]+s[23:], '%Y-%m-%dT%H:%M:%S%z')

def extractPeriod(layoutEl):
    """Returns a Dictonary in the format {name, starts, ends}
    where each is the key to a list
    """
    startEls = layoutEl.findall('./start-valid-time')
    endEls = layoutEl.findall('./end-valid-time')

    # gather relevent info as lists
    startTimes = map(lambda el: xml2date(el.text), startEls)
    endTimes = map(lambda el: xml2date(el.text), endEls)
    names = map(lambda el: el.get('period-name'), startEls)

    return {'names': list(names), 'starts': list(startTimes), 'ends': list(endTimes)}

def getLayouts(root):
    assert isinstance(root, ET.Element)
    layoutEls = root.findall("./data/time-layout")

    getKey = lambda layoutEl: layoutEl.findtext('layout-key')

    layouts = {getKey(el): extractPeriod(el) for el in layoutEls}

    return layouts

def dwml2json(root):
    """
    Converts DWML formatted forcast from the NWS and extracts relevant
    information in the format readable by the website.

    :param root: (ElementTree.Element) The root element in DWML file
    :return: (str) JSON of fromatted DWML (XML) forcast
    """
    baseLayout = "k-p12h-n14-3"
    assert isinstance(root, ET.Element)

    layouts = getLayouts(root)

    # baseLayout is used as the model for the layout on the website
    forecastList = [OrderedDict([('period', period)]) for period in layouts[baseLayout]['names']]

    for forecast, start, end in zip(
            forecastList,
            layouts[baseLayout]['starts'],
            layouts[baseLayout]['ends']):

        forecast['start'] = str(start)
        forecast['end'] = str(end)

    # get MAX temperature forecast
    key = root.find("./data/parameters/temperature[@type='maximum']").get('time-layout')
    for i, els in enumerate(root.findall("./data/parameters/temperature[@type='maximum']/value")):
        # try to find matching time frame for temp layout and base layout
        try:
            match = layouts[baseLayout]['starts'].index(layouts[key]['starts'][i])
            forecastList[match]['max']= int(els.text)
        except (ValueError, TypeError):
            continue

    # get MIN temperature forecast
    key = root.find("./data/parameters/temperature[@type='minimum']").get('time-layout')
    for i, els in enumerate(root.findall("./data/parameters/temperature[@type='minimum']/value")):
        # try to find matching time frame for temp layout and base layout
        try:
            match = layouts[baseLayout]['starts'].index(layouts[key]['starts'][i])
            forecastList[match]['min']= int(els.text)
        except (ValueError, TypeError):
            continue

    # get Precipitation chances
    key = root.find("./data/parameters/probability-of-precipitation").get('time-layout')
    for i, els in enumerate(root.findall(
                    "./data/parameters/probability-of-precipitation[@time-layout='%s']/value" % key)):
        try:
            match = layouts[baseLayout]['starts'].index(layouts[key]['starts'][i])
            forecastList[match]['precip'] = int(els.text)
        except (ValueError, TypeError):
            continue

    # get weather conditions
    key = root.find("./data/parameters/weather").get('time-layout')
    for i, els in enumerate(root.findall(
                    "./data/parameters/weather[@time-layout='%s']/weather-conditions" % key)):
        try:
            match = layouts[baseLayout]['starts'].index(layouts[key]['starts'][i])
            forecastList[match]['conditions'] = els.get('weather-summary')
        except (ValueError, TypeError):
            continue

    # get weather condition icon links
    key = root.find("./data/parameters/conditions-icon").get('time-layout')
    for i, els in enumerate(root.findall(
                    "./data/parameters/conditions-icon[@time-layout='%s']/icon-link" % key)):
        try:
            match = layouts[baseLayout]['starts'].index(layouts[key]['starts'][i])
            forecastList[match]['icon'] = els.text
        except (ValueError, TypeError):
            continue

    return json.dumps(forecastList, indent=2)

def updateForecast(forecastObj):
    """
    The latest NWS forecast information will be extracted and stored
    into the database as a JSON string.
    :param forecastObj: Django Forecast model object.
    """
    #set up logger to print info message
    formatter = logging.Formatter("%(module)s: %(levelname)s: %(asctime)s - %(message)s")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    sh.setLevel(logging.INFO)
    logger.addHandler(sh)

    logger.info("Downloading the latest NWS forecast "
                "information for " + forecastObj.location)

    # extract NWS data from SOAP server
    client = SOAPClient(SOAP_URL)

    # definition:
    # NDFDgenByDay(lat, lon, startDate, numDays, Units, format)
    # returns a string representing the xml data results
    results = client.service.NDFDgenByDay(
        str(forecastObj.lat),  # lat
        str(forecastObj.lon),  # lon
        '',  # startDate (unnecessary for full 7 day forecasting)
        str(forecastObj.days),  # numDays
        'e',  # Unit (either 'e' for english standard or 'm' for metric)
        '%i hourly' % forecastObj.hours  # format, either '12 hourly' or '24 hourly (e.i. 6:00 AM - 6:00 AM)'
    )

    # use ElementTree to parse returned xml string
    root = ET.fromstring(results)

    # Convert the Element of the DWML xml object into a JSON string
    forecastObj.json_forecast=dwml2json(root)

    forecastObj.refreshed=datetime.now()
    forecastObj.clean()
    forecastObj.save()

# TODO
def updateHazards():
    pass