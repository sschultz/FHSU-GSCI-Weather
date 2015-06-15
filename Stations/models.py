from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ValidationError

DISTANCE_UNITS = (
    ('mm', 'Millimeters'),
    ('cm', 'Centimeters'),
    ('m', 'Meters'),
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
    ('BP',     'Barometric Pressure'),
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
    name = models.CharField(max_length=254,
                            unique=True,
                            help_text="Spaces are not allowed. The name "
                                      "should match the field name of the "
                                      "imported data.")
    description = models.TextField(blank=True)
    slug = models.SlugField(primary_key=True)
    location = models.TextField(blank=True)
    date_installed = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=False)
    contact = models.EmailField(max_length=254, blank=True)
    logger_interval = models.IntegerField(
        help_text="Seconds per Sensor Reading"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Sensor(models.Model):
    name = models.CharField(max_length=80)
    sensor_type = models.CharField(max_length=10, choices=SENSOR_TYPE)
    description = models.TextField(blank=True)
    station = models.ForeignKey(Station)
    data_unit = models.CharField(max_length=10)
    height = models.IntegerField(null=True, blank=True)
    height_unit = models.CharField(max_length=2, choices=DISTANCE_UNITS,
                                   blank=True)
    slug = models.SlugField()
    frontPage = models.BooleanField(default=False,
                                    help_text="Will display on the station's "
                                    "front page by default")

    def __str__(self):
        return "%s - %s" % (self.station.name, self.slug)

    def validate_unique(self, exclude=None):
        # get the number of sensors with the same slug
        # on this station
        nObjs_slug = Sensor.objects.filter(
            slug=self.slug,
            station=self.station
        ).exclude(pk=self.pk).count()

        # get the number of sensors with the same name
        # on this station
        nObjs_name = Sensor.objects.filter(
            name=self.name,
            station=self.station
        ).exclude(pk=self.pk).count()

        # if a sensor with the same name or slug already exists:
        # raise the appropriate error.
        if nObjs_name > 0:
            raise ValidationError({
                'name':[ValidationError(
                    message='Another sensor with name "' + str(self.name) +
                    '" already exists on the ' + self.station.name + ' station.',
                    code='unique',
                    params={},
                )]
            })
        if nObjs_slug > 0:
            raise ValidationError({
                'slug':[ValidationError(
                    message='Another sensor with the slug "' + str(self.slug) +
                    '" already exists on the ' + self.station.name + ' station.',
                    code='unique',
                    params={},
                )]
            })

    class Meta:
        ordering = ['station__name', 'sensor_type', 'name']


class SensorData(models.Model):
    timestamp = models.DateTimeField(db_index=True)
    sensor = models.ForeignKey(Sensor)
    val_type = models.CharField(max_length=3, choices=VALUE_TYPE)
    val = models.FloatField()

    def __str__(self):
        return self.sensor.name+':'+self.val_type + '@' + \
            str(self.timestamp) + ' = '+str(self.val)

    def validate_unique(self, exclude=None):
        objs = SensorData.objects.filter(
            timestamp=self.timestamp,
            sensor=self.sensor,
            val_type=self.val_type)
        if len(objs) > 0:
            raise ValidationError("Overlapping data at same time '" +
                                  self.timestamp + "' on sensor " +
                                  self.sensor.name +
                                  ' (' + self.sensor.slug + ')')
