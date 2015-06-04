from django.db import models

HOURLY_TYPE = (
    (12, '12 Hour'),
    (24, '24 Hour')
)

# A forecast table to contain the latest forecast and the last refresh time from NWS
class Forecast(models.Model):
    days = models.PositiveIntegerField(
        null=False,
        help_text='How many days included in the forecast',
        default=7
    )
    hours = models.PositiveIntegerField(
        help_text='12 Hour or 24 Hour Forecast',
        choices=HOURLY_TYPE,
        null=False,
        default=12
    )
    refreshed = models.DateTimeField(
        help_text='Data was last refreshed on this date',
        null=True,
        editable=False
    )

    location = models.TextField(editable=False, help_text="Location Display Name")
    lat = models.FloatField(verbose_name='Latitude', null=False)
    lon = models.FloatField(verbose_name='Longitude', null=False)

    json_forecast = models.TextField(
        help_text="Website readable JSON text",
        blank=False,
        null=True,
        editable=False
    )
    json_alerts = models.TextField(
        default=None,
        help_text="Alerts/Warnings/Advisories from the NWS",
        editable=False,
        null=True
    )

    def __str__(self):
        return "%i day %i hour forecast for %s retrieved on %s" %\
               (self.days, self.hours, self.location, str(self.refreshed))

    class Meta:
        ordering = ['location']
        index_together = [['days', 'hours']]

class WMSRadarOverlay(models.Model):
    display_name = models.TextField(blank=False, null=False)
    url = models.URLField(blank=False, null=False)
    layers = models.TextField(blank=False, null=False, help_text="Comma separated list of layers to be pulled")
    tile_width = models.PositiveIntegerField(default=256)
    tile_height = models.PositiveIntegerField(default=256)
    version = models.CharField(default="1.1.1", max_length=10, verbose_name="WMS Version")
    update_period = models.PositiveIntegerField(
        default=5,
        help_text="How long (in minutes) does it take to update"
    )
    format = models.TextField(default="image/png")
    coordsys = models.TextField(
        default="EPSG:4326",
        help_text="Example Reference: http://spatialreference.org/ref/epsg/wgs-84/"
    )
    active = models.BooleanField(default=False, null=False, help_text="Whether to display this overlay or not")
    credit = models.TextField(blank=True)
    legend_url = models.URLField(null=True, default=None)

    def __str__(self):
        return str(self.display_name) + " (%s)" % str(self.layers)

    class Meta:
        verbose_name = "WMS Radar Overlay"