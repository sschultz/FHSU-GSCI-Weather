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
            update_period=5,
            credit='NEXRAD Composites Courtesy of '
                   '<a href="http://mesonet.agron.iastate.edu/docs/nexrad_composites/">'
                   'Iowa State University\'s Iowa Environmental Mesonet</a>',
            logo="http://mesonet.agron.iastate.edu/images/logo_small.png",
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
            update_period=5,
            credit='NEXRAD Composites Courtesy of the '
                   '<a href="http://www.weather.gov/">'
                   'National Weather Service</a>',
            logo="http://w2.weather.gov/images/climate/nwsright.jpg",
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