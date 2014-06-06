from django.contrib import admin
from stations.models import Station, Sensor

class StationAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}

class SensorAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('sensor_type','height',)}

# Register your models here.
admin.site.register(Station, StationAdmin)
admin.site.register(Sensor, SensorAdmin) 
