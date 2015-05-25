from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from Weather.models import Forecast

HaysLat, HaysLon = '38.885425', '-99.317830'
HaysLocationName = "Hays, KS"

class Command(BaseCommand):
    help = "Initialize forecast table with Hays, KS information"

    def handle(self, *args, **options):
        # check if table entry already exists
        try:
            Forecast.objects.get(location=HaysLocationName)
        except ObjectDoesNotExist:
            print("Creating forecast entry for Hays, KS...")
            self.initHaysForecast()
            return

        print("Hays, KS entry already exists")
        return

    def initHaysForecast(self):
        obj = Forecast.objects.create(
            location=HaysLocationName,
            lat=float(HaysLat),
            lon=float(HaysLon),
            days=7,
            hours=12,
        )
        obj.clean()
        obj.save()

        print("Finished")