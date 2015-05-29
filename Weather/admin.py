from django.contrib import admin
from Weather.models import *
from Weather.util import updateForecast


def update_forecast(modeladmin, request, queryset):
    for forecast in queryset:
        updateForecast(forecast)

update_forecast.short_description = "Force forecast update from NWS"


class forecastAdmin(admin.ModelAdmin):
    actions = [update_forecast]


class WMSRadarOverlayAdmin(admin.ModelAdmin):
    pass


admin.site.register(Forecast, forecastAdmin)
admin.site.register(WMSRadarOverlay, WMSRadarOverlayAdmin)