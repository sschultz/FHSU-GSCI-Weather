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
    latitude = models.DecimalField(
        blank=True, null=True,
        max_digits=10,
        decimal_places=6,
        help_text="Datum: WGS84",
        default=None
    )
    longitude = models.DecimalField(
        blank=True, null=True,
        max_digits=10,
        decimal_places=6,
        help_text="Datum: WGS84",
        default=None
    )
    elevation = models.IntegerField(
        blank=True, null=True,
        help_text="Elevation of MET base in meters from sea level"
    )
    date_installed = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=False)
    contact = models.EmailField(max_length=254, blank=True)
    logger_interval = models.IntegerField(
        help_text="Seconds per Sensor Reading"
    )

    def clean_longitude(self):
        pass

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Sensor(models.Model):
    name = models.CharField(
        max_length=80,
        help_text="Identifier that relates to the import method (e.g. csv field name)"
    )
    display_name = models.CharField(
        max_length=80,
        blank=True, null=True,
        default=None,
        help_text="Sensor name will be used as display value if this value is empty"
    )
    sensor_type = models.CharField(max_length=10, choices=SENSOR_TYPE)
    description = models.TextField(blank=True)
    station = models.ForeignKey(Station)
    data_unit = models.CharField(max_length=10)
    height = models.IntegerField(
        null=True,
        blank=True,
        help_text="height of instrument above the MET base"
    )
    height_unit = models.CharField(max_length=2, choices=DISTANCE_UNITS,
                                   blank=True)
    slug = models.SlugField()
    frontPage = models.BooleanField(default=False,
                                    help_text="Will display on the station's "
                                    "front page by default")

    def __str__(self):
        return "%s - %s" % (self.station.name, self.slug)

    def get_display_field(self):
        if self.display_name is None:
            return self.name
        return self.display_name

    def get_formatted_name(self):
        fmt = "%s"
        if self.height is None or self.display_name is None:
            return fmt % str(self.get_display_field())
        fmt += " (%i%s)"
        return fmt % (
            str(self.get_display_field()),
            int(self.height),
            str(self.height_unit)
        )

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
            val_type=self.val_type
        )

        # Ignore self if part of table
        objs = objs.exclude(pk=self.pk)

        if objs.count() > 0:
            raise ValidationError({
                '':[ValidationError(
                    message="Overlapping data at same time '" +
                            str(self.timestamp) + "' on sensor " +
                            self.sensor.name +
                            ' (' + self.sensor.slug + ')',
                    code='unique',
                    params={}
                )]
            })