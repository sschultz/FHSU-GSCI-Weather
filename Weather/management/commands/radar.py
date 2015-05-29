from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from Weather.models import WMSRadarOverlay


def init_radar_overlays():
    LayerName = "Doppler Radar"
    try:
        WMSRadarOverlay.objects.get(display_name=LayerName)

    except ObjectDoesNotExist:
        obj = WMSRadarOverlay.objects.create(
            display_name=LayerName,
            url=r"http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r-t.cgi",
            layer=r"nexrad-n0r-wmst",
            tile_width=256,
            tile_height=256,
            update_period=5,
            format="image/png",
            coordsys="EPSG:4326",
            active=True
        )
        obj.clean()
        obj.save()

        print(LayerName + " WMS Overlay Entry Added")

    else:
        print(LayerName + " WMS Overlay already exists.")
        print("Nothing to do")


class Command(BaseCommand):
    help = "Manage radar map information"

    option_list = BaseCommand.option_list + (
        make_option('--init',
                    action='store_true',
                    dest='init',
                    default=False,
                    help='Initialize radar info with '
                         'default overlays/layers'),
    )

    def handle(self, *args, **options):
        if options['init']:
            init_radar_overlays()
        else:
            print("Nothing to do")