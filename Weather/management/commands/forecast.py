from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from Weather.models import Forecast
from Weather.util import updateForecast

HaysLat, HaysLon = '38.885425', '-99.317830'
HaysLocationName = "Hays, KS"

class Command(BaseCommand):
    help = "Manage forecast information"

    option_list = BaseCommand.option_list + (
        make_option('--init',
                    action='store_true',
                    dest='init',
                    default=False,
                    help='Initialize forecast table with '
                         'Hays, KS information'),
        make_option('--update-now',
                    action='store_true',
                    dest='update-now',
                    default=False,
                    help='Connect to NWS and download latest '
                         'forecast information')
        )

    def handle(self, *args, **options):
        if options['init']:
            # check if table entry already exists
            try:
                Forecast.objects.get(location=HaysLocationName)
            except ObjectDoesNotExist:
                print("Creating forecast entry for Hays, KS...")
                self.initHaysForecast()
                return

            print("Hays, KS entry already exists")
            return
        elif options['update-now']:
            self.forceUpdate()
        else:
            print("Nothing to do")

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

    def forceUpdate(self):
        objs = Forecast.objects.all()
        for obj in objs:
            updateForecast(obj)

        print("Update Complete!")
