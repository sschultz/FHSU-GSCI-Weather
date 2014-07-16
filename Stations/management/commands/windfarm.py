from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from optparse import make_option
from Stations.models import Station, Sensor, SensorData
from pycampbellcr1000 import CR1000


class Command(BaseCommand):
    """A manage.py command for managing the windfarm data"""
    help = 'Manage FHSU Windfarm dataset'

    option_list = BaseCommand.option_list + (
        make_option('--create',
                    action='store_true',
                    dest='create',
                    default=False,
                    help='Create station and sensors related to the windfarm '
                    'station'),
        make_option('--update-now',
                    action='store_true',
                    dest='update-now',
                    default=False,
                    help='Connect to the windfarm datalogger and download '
                    'any data since most recent data timestamp')
        )

    def handle(self, *args, **options):
        if options['create']:
            self.CreateWindfarm()
        if options['update-now']:
            self.UpdateNow()

    def CreateWindfarm(self):
        """Create database station entry with all applicable sensors"""
        try:
            windfarm = Station('Windfarm',
                               'FHSU Weather tower next to the SuperDARN',
                               'windfarm', '',
                               '2013-07-10', True, '', 600)

            windfarm.full_clean()
            windfarm.save()
        except:
            raise CommandError("Unable to create 'Windfarm' station. "
                               "Perhapse it already exists?")

        #Enter all sensor information
        bat = Sensor(name='Batt_Volt', sensor_type='Bat', station=windfarm,
                     description='Battery voltage reading',
                     data_unit='V', slug='battery')
        bat.full_clean()
        bat.save()

        ws60prim = Sensor(name='WS_C1_60m_Prim', sensor_type='WS',
                          station=windfarm,
                          description='Wind Speed at 60m',
                          data_unit='m/s', height=60, height_unit='m',
                          slug='ws60')

        ws60prim.full_clean()
        ws60prim.save()

#needs reformatted as per pep8
        ws60redun = Sensor(name='WS_C1_60m_Redun', sensor_type='WS', station=windfarm,
            description='Redundant Wind Speed Sensor at 60m',
            data_unit='m/s', height=60, height_unit='m', slug='ws60redun')

        ws60redun.full_clean()
        ws60redun.save()

        ws50prim = Sensor(name='WS_C1_50m_Prim',sensor_type='WS', station=windfarm,
            description='Wind Speed at 50m',
            data_unit='m/s', height=50, height_unit='m', slug='ws50')

        ws50prim.full_clean()
        ws50prim.save()

        ws40prim = Sensor(name='WS_C1_40m_Prim',sensor_type='WS', station=windfarm,
            description='Wind Speed at 40m',
            data_unit='m/s', height=40, height_unit='m', slug='ws40')

        ws40prim.full_clean()
        ws40prim.save()

        ws40redun = Sensor(name='WS_C1_40m_Redun',sensor_type='WS', station=windfarm,
            description='Redundant Wind Speed Sensor at 40m',
            data_unit='m/s', height=40, height_unit='m', slug='ws40redun')

        ws40redun.full_clean()
        ws40redun.save()

        ws10prim = Sensor(name='WS_C1_10m_Prim',sensor_type='WS', station=windfarm,
            description='Wind Speed at 10m',
            data_unit='m/s', height=10, height_unit='m', slug='ws10', frontPage=True)
        ws10prim.full_clean()
        ws10prim.save()

        wd59 = Sensor(name='WD_200P_59m',sensor_type='WD', station=windfarm,
            description='Wind Direction at 59m from the ground',
            data_unit='deg', height=59, height_unit='m', slug='wd59')

        wd59.full_clean()
        wd59.save()

        wd49 = Sensor(name='WD_200P_49m',sensor_type='WD', station=windfarm,
            description='Wind Direction at 49m from the ground',
            data_unit='deg', height=49, height_unit='m', slug='wd49')

        wd49.full_clean()
        wd49.save()

        tmp5 = Sensor(name='Tmp_110S_5ft', sensor_type='Temp', station=windfarm,
            description='Temperature at 5ft from ground',
            data_unit='C', height=5, height_unit='ft', slug='tmp5', frontPage=True)

        tmp5.full_clean()
        tmp5.save()

        tmp10 = Sensor(name='Tmp_110S_10ft', sensor_type='Temp', station=windfarm,
            description='Temperature at 10ft from ground',
            data_unit='C', height=10, height_unit='ft', slug='tmp10')
        tmp10.full_clean()
        tmp10.save()

        rh5 = Sensor(name='RH_RH5_5ft', sensor_type='RH', station=windfarm,
            description='Relative Humidity at 5ft from ground',
            data_unit='%', height=5, height_unit='ft', slug='rh5')
        rh5.full_clean()
        rh5.save()

        rh10 = Sensor(name='RH_RH5_10ft', sensor_type='RH', station=windfarm,
            description='Relative Humidity at 10ft from ground',
            data_unit='%', height=10, height_unit='ft', slug='rh10')
        rh10.full_clean()
        rh10.save()

        bp = Sensor(name='BP_BP20_5ft', sensor_type='BP', station=windfarm,
            description='Barometric Pressure',
            data_unit='kPa', height=5, height_unit='ft', slug='bp', frontPage=True)
        bp.full_clean()
        bp.save()

        precip = Sensor(name='Precip_NVL_5ft', sensor_type='Precip', station=windfarm,
            description='Precipitation',
            data_unit='mm', height=5, height_unit='ft', slug='precip')
        precip.full_clean()
        precip.save()

        solrad_lp02 = Sensor(name='Solar_Rad_LP02_5ft', sensor_type='Rad', station=windfarm,
            description='LP02 Solar Radiation',
            data_unit='Wm^2', height=5, height_unit='ft', slug='rad-lp02')
        solrad_lp02.full_clean()
        solrad_lp02.save()

        solrad_nr2 = Sensor(name='Solar_Rad_NR2_5ft', sensor_type='Rad', station=windfarm,
            description='Solar Radiation',
            data_unit='Wm^2', height=5, height_unit='ft', slug='rad-nr2')
        solrad_nr2.full_clean()
        solrad_nr2.save()

        print("Windfarm station created")

    def UpdateNow(self):
        addr = "tcp:ip:port"
        print("UNFINISHED: TODO")
        return

        try:
            start = SensorData.objects.latest('timestamp').timestamp
        except ObjectDoesNotExist:
            print("No prevouse data records found.")
            print("Downloading all logger data...")
            device = CR1000.from_url(addr)
            dataList = device.get_data('Ten_Min')
        else:
            print("Beginning download of all data recorded since " +
                  str(start))
            device = CR1000.from_url(addr)
            dataList = device.get_data('Ten_Min', start)

        toSaveList = []
        for record in dataList:
            ts = record['TIMESTAMP']
            del record['TIMESTAMP']
            for val, col in record.items():
                try:
                    dat = SensorData(
                        sensor=None,
                        timestamp=ts,
                        val_type=None,
                        val=float(val))
                    dat.full_clean()
                    toSaveList.append(dat)
                except:
                    continue

        for dat in toSaveList:
            dat.save()
