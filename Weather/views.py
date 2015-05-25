from django.shortcuts import render
from django.http import HttpResponse
from django.core import exceptions as django_ex
from Weather.models import Forecast as ForecastModel
from Weather.util import updateForecast
from datetime import datetime, timedelta


def radarView(request):
    return render(request, 'radar.html', {})


def forecastView(request):
    # check if NWS forecast data needs updated
    # only update once every 2 hours
    obj = ForecastModel.objects.get(days=7, hours=12, location='Hays, KS')
    if obj.refreshed == None or \
        datetime.now() - obj.refreshed > timedelta(hours=2):

        updateForecast(obj)

    return HttpResponse(obj.json_forecast, content_type="application/json")