from django.db import models

DISTANCE_UNITS = (
    ('mm', 'Millimeters'),
    ('cm', 'Centimeters'),
    ('m' , 'Meters'),
    ('km', 'Kilometers'),
    ('NM', 'Nautical Miles'),
    ('in', 'Inches'),
    ('ft', 'Feet'),
    ('yd', 'Yards'),
    ('mi', 'Miles'),
)

SENSOR_TYPE = (
    ('Temp',   'Temperature'),
    ('WS',     'Wind Speed'),
    ('WD',     'Wind Direction'),
    ('Pres',   'Pressure'),
    ('RH',     'Relative Humidity'),
    ('Precip', 'Percipitation'),
    ('Rad',    'Solar Radiation'),
    ('Bat',    'Battery'),
)

class Station(models.Model):
    name            = models.CharField(max_length=254)
    description = models.TextField(blank=True)
    slug            = models.SlugField(primary_key=True)
    location        = models.TextField(blank=True)
    date_installed  = models.DateField(null=True, blank=True)
    active          = models.BooleanField()
    contact         = models.EmailField(max_length=254, blank=True)
    logger_interval = models.IntegerField(help_text="Sensor Readings per Second")

    def __unicode__(self):
        return self.name

class Sensor(models.Model):
    name      = models.CharField(max_length=80)
    sensor_type = models.CharField(max_length=10, choices=SENSOR_TYPE)
    description = models.TextField(blank=True)
    station   = models.ForeignKey(Station)
    data_unit = models.CharField(max_length=10)
    height    = models.IntegerField(null=True, blank=True)
    heightUnits = models.CharField(max_length=2, choices=DISTANCE_UNITS, blank=True)
    slug      = models.SlugField()

    def __unicode__(self):
        return self.slug

    class META:
        unique_together = (('slug','station'),('name','station'),)

class SensorData(models.Model):
    sensor    = models.ForeignKey(Sensor)
    timestamp = models.DateTimeField(db_index=True)
    avg       = models.FloatField(help_text="Average value over interval measured")

    def __unicode__(self):
        return self.avg

    class META:
        unique_together = (('sensor','timestamp'),)

#For sensor data that records minimum and maximum readings over an interval
class SensorStatData(SensorData):
    min_val = models.FloatField()
    max_val = models.FloatField()
    std     = models.FloatField()

class SensorStatTotalData(SensorStatData):
    total = models.FloatField()
