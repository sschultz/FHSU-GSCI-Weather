from django.shortcuts import render
from django.http import HttpResponse
from django.core import exceptions as django_ex
from Weather.models import Forecast as ForecastModel
from Weather.util import updateHaysForecast
from Weather.util import forecastDBname
from datetime import datetime, timedelta


def radarView(request):
    return render(request, 'radar.html', {})


def forecastView(request):
    # check if NWS forecast data needs updated
    # only update once every 2 hours
    try:
        obj = ForecastModel.objects.get(type=forecastDBname)
        if datetime.now() - obj.refreshed > timedelta(hours=2):
            updateHaysForecast()
    except django_ex.ObjectDoesNotExist:
        # updateHaysForecast will create the forecast table entry
        updateHaysForecast()
        obj = ForecastModel.objects.get(type=forecastDBname)

    HttpResponse(obj.json_str, content_type="application/json")