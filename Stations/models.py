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

VALUE_TYPE = (
    ('AVG', 'Average'),
    ('TOT', 'Total'),
    ('MIN', 'Minimum'),
    ('MAX', 'Maximum'),
    ('STD', 'Standard Deviation'),
)

class Station(models.Model):
    name            = models.CharField(max_length=254, help_text="Spaces are not allowed. The name should match the field name of the imported data.")
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
    height_unit = models.CharField(max_length=2, choices=DISTANCE_UNITS, blank=True)
    slug      = models.SlugField()

    def __unicode__(self):
        return self.slug

    class META:
        unique_together = (('slug','station'),('name','station'),)

class SensorRecord(models.Model):
    sensor    = models.ForeignKey(Sensor)
    timestamp = models.DateTimeField(db_index=True)
    
    val       = models.FloatField(help_text="Average value or Total value over interval measured")

    def __unicode__(self):
        return self.timestamp

    class META:
        unique_together = (('sensor','timestamp'),)

class SensorData(models.Model):
    record = models.ForeignKey(SensorRecord)
    val_type = models.CharField(max_length = 3, choices=VALUE_TYPE)
    val = models.FloatField()

    def __unicode__(self):
        return unicode(self.val)

    class META:
        unique_together = (('record','val_type'),)
