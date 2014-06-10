from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from Stations.models import Station, Sensor, SensorData, SensorStatData, SensorStatTotalData

class Command(BaseCommand):
    help = 'Manage FHSU Windfarm dataset'

    option_list = BaseCommand.option_list + (
        make_option('--create',
            action='store_true',
            dest='create',
            default=False,
            help='Create station and sensors related to the windfarm station'),
        make_option('--update-now',
            action='store_true',
            dest='update-now',
            default=False,
            help='Connect to the windfarm datalogger and download any data since most recent data timestamp')
        )

    def handle(self, *args, **options):
        if options['create']:
            self.CreateWindfarm()
        if options['update-now']:
            self.UpdateNow()

    def CreateWindfarm(self):
        windfarm = Station('Windfarm',
            'FHSU Weather tower next to the SuperDARN',
            'windfarm', '',
            '2013-07-10', True, '', 600)
        windfarm.save()

        bat = Sensor(name='Batt_Volt_Min', sensor_type='Bat', station=windfarm,
            description='Battery minimum voltage reading',
            data_unit='V', slug='batt')
        bat.save()

        ws60prim = Sensor(name='WS_C1_60m_Prim',sensor_type='WS', station=windfarm,
            description='Wind Speed at 60m',
            data_unit='m/s', height=60, heightUnits='m', slug='ws60')
        ws60prim.save()

        ws60redun = Sensor(name='WS_C1_60m_Redun',sensor_type='WS', station=windfarm,
            description='Redundant Wind Speed Sensor at 60m',
            data_unit='m/s', height=60, heightUnits='m', slug='ws60redun')
        ws60redun.save()

        ws50prim = Sensor(name='WS_C1_50m_Prim',sensor_type='WS', station=windfarm,
            description='Wind Speed at 50m',
            data_unit='m/s', height=50, heightUnits='m', slug='ws50')
        ws50prim.save()
        
        ws40prim = Sensor(name='WS_C1_40m_Prim',sensor_type='WS', station=windfarm,
            description='Wind Speed at 40m',
            data_unit='m/s', height=40, heightUnits='m', slug='ws40')
        ws40prim.save()

        ws40redun = Sensor(name='WS_C1_40m_Redun',sensor_type='WS', station=windfarm,
            description='Redundant Wind Speed Sensor at 40m',
            data_unit='m/s', height=40, heightUnits='m', slug='ws40redun')
        ws40redun.save()

        ws10prim = Sensor(name='WS_C1_10_Prim',sensor_type='WS', station=windfarm,
            description='Wind Speed at 10m',
            data_unit='m/s', height=10, heightUnits='m', slug='ws10')
        ws10prim.save()

        wd_sd = Sensor(name='WD_200P_59m_SD',sensor_type='WD', station=windfarm,
            description='Wind Direction at 59m from ground',
            data_unit='rad', height=59, heightUnits='m', slug='WD-sd')
        wd_sd.save()

        wd_wvt = Sensor(name='WD_200P_49m_WVT',sensor_type='WD', station=windfarm,
            description='Wind Direction at 49m from ground',
            data_unit='rad', height=49, heightUnits='m', slug='wd-wvt')
        wd_wvt.save()

        tmp5 = Sensor(name='Tmp_110S_5ft', sensor_type='Temp', station=windfarm,
            description='Temperature at 5ft from ground',
            data_unit='C', height=5, heightUnits='ft', slug='tmp5')
        tmp5.save()

        tmp10 = Sensor(name='Tmp_110S_10ft', sensor_type='Temp', station=windfarm,
            description='Temperature at 10ft from ground',
            data_unit='C', height=10, heightUnits='ft', slug='tmp10')
        tmp10.save()

#       PTemp_C,WS_C1_60m_Prim_Avg,WS_C1_60m_Prim_Max,WS_C1_60m_Prim_Min,WS_C1_60m_Prim_Std,WS_C1_60m_Redun_Avg,WS_C1_60m_Redun_Max,WS_C1_60m_Redun_Min,WS_C1_60m_Redun_Std,WS_C1_50m_Prim_Avg,WS_C1_50m_Prim_Max,WS_C1_50m_Prim_Min,WS_C1_50m_Prim_Std,WS_C1_40m_Prim_Avg,WS_C1_40m_Prim_Max,WS_C1_40m_Prim_Min,WS_C1_40m_Prim_Std,WS_C1_40m_Redun_Avg,WS_C1_40m_Redun_Max,WS_C1_40m_Redun_Min,WS_C1_40m_Redun_Std,WS_C1_10m_Prim_Avg,WS_C1_10m_Prim_Max,WS_C1_10m_Prim_Min,WS_C1_10m_Prim_Std,WD_200P_59m_WVT,WD_200P_59m_SD,WD_200P_49m_WVT,WD_200P_49m_SD,Tmp_110S_5ft_Avg,Tmp_110S_5ft_Max,Tmp_110S_5ft_Min,Tmp_110S_5ft_Std,Tmp_110S_10ft_Avg,Tmp_110S_10ft_Max,Tmp_110S_10ft_Min,Tmp_110S_10ft_Std,RH_RH5_5ft_Avg,RH_RH5_5ft_Max,RH_RH5_5ft_Min,RH_RH5_5ft_Std,RH_RH5_10ft_Avg,RH_RH5_10ft_Max,RH_RH5_10ft_Min,RH_RH5_10ft_Std,BP_BP20_5ft_Avg,BP_BP20_5ft_Max,BP_BP20_5ft_Min,BP_BP20_5ft_Std,Precip_NVL_5ft_Tot,Solar_Rad_LP02_5ft_Avg,Solar_Rad_LP02_5ft_Max,Solar_Rad_LP02_5ft_Min,Solar_Rad_LP02_5ft_Std,Solar_Rad_LP02_5ft_Tot,Solar_Rad_NR2_5ft_Avg,Solar_Rad_NR2_5ft_Max,Solar_Rad_NR2_5ft_Min,Solar_Rad_NR2_5ft_Std,Solar_Rad_NR2_5ft_Tot


    def UpdateNow(self):
        print("TODO: Windfarm.UpdateNow()")
