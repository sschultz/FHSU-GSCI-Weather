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
    layers = models.TextField(
        blank=False,
        null=False,
        help_text="Comma separated list of layers to be pulled"
    )

    update_period = models.PositiveIntegerField(
        default=5,
        help_text="How long (in minutes) does it take to update"
    )

    active = models.BooleanField(
        default=False,
        null=False,
        help_text="Whether to display this overlay or not"
    )
    credit = models.TextField(blank=True, help_text="HTML credits to this datasource")
    legend_url = models.URLField(null=True, blank=True, default=None)
    logo = models.URLField(null=True, blank=True, default=None)
    order = models.PositiveIntegerField(
        default=5,
        help_text="Layer draw order, A higher order overlay will be drawn over a lower order overlay"
    )

    def __str__(self):
        return str(self.display_name) + " (%s)" % str(self.layers)

    class Meta:
        verbose_name = "WMS Radar Overlay"
        ordering = ["order"]