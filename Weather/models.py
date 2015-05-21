from django.db import models


# A forecast table to contain the latest forecast and the last refresh time from NWS
class Forecast(models.Model):
    type = models.TextField(
        editable=False,
        blank=False,
        null=False,
        help_text='Example: Hourly, 3 Day 12 Hour, 7 Day 24 Hour, etc'
    )
    refreshed = models.DateTimeField(null=False, blank=False)
    json_str = models.TextField(null=False)

    def __str__(self):
        return str(self.type) + ' forecast retrieved on ' + str(self.refreshed)