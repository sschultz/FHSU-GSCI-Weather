from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from Weather.models import WMSRadarOverlay


def init_radar_overlays():
    RadarLayerName = "NEXRAD Doppler Radar"
    AltRadarLayerName = "NWS RIDGE Radar"

    try:
        WMSRadarOverlay.objects.get(display_name=RadarLayerName)
        print(RadarLayerName + " WMS Overlay already exists.")

    except ObjectDoesNotExist:
        obj = WMSRadarOverlay.objects.create(
            display_name=RadarLayerName,
            url=r"http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r-t.cgi",
            layers=r"nexrad-n0r-wmst",
            tile_width=256,
            tile_height=256,
            update_period=5,
            format="image/png",
            coordsys="EPSG:4326",
            credit="Iowa State University",
            legend_url=None,
            active=True
        )
        obj.clean()
        obj.save()

        print(RadarLayerName + " WMS Overlay Entry Added")

    try:
        WMSRadarOverlay.objects.get(display_name=AltRadarLayerName)
        print(AltRadarLayerName + " WMS Overlay already exists.")

    except ObjectDoesNotExist:
        obj = WMSRadarOverlay.objects.create(
            display_name=AltRadarLayerName,
            url=r"http://gis.srh.noaa.gov/arcgis/services/RIDGERadar/MapServer/WMSServer",
            layers=r"0",
            tile_width=256,
            tile_height=256,
            update_period=5,
            format="image/png",
            coordsys="EPSG:4326",
            credit="National Weather Service",
            legend_url="http://gis.srh.noaa.gov/arcgis/services/RIDGERadar/MapServer/WMSServer?request=GetLegendGraphic&version=1.1.1&format=image/png&layer=0",
            active=False
        )

        obj.clean()
        obj.save()

        print(AltRadarLayerName + " WMS Overlay Entry Added")

    print("Done")


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