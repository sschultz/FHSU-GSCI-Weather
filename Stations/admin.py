from django.contrib import admin
from Stations.models import Station, Sensor


class StationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class SensorAdmin(admin.ModelAdmin):
        repopulated_fields = {
            'slug': ('sensor_type', 'height',),
            'display_name': ('abc',)
        }

# Register your models here.
admin.site.register(Station, StationAdmin)
admin.site.register(Sensor, SensorAdmin)
