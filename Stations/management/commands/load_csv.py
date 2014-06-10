from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from csv import DictReader
import Stations.models

class Command(BaseCommand):
    args = '<StationName filename>'
    help = 'Loads station sensor data from a CSV file.  If --mapfile is not specified then the CSV file header (first line of CSV file) must contain matching sensor names belonging to specified station.'

    option_list = BaseCommand.option_list + (
            make_option('--mapfile',
                action='store',
                dest='mapfile',
                default='',
                help='{ --mapfile filename } specify a file containing a list that maps station sensor names (database table columns) to csv columns.  This file can either be a list containing Station.Sensor names, or the file can be a list containing Station.Sensor = CSVColName.'),
        )

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError('Must only have 2 argurments (station_name and filename)')
        with DictReader(open(args[1],'r')) as csvFile:
                for row in csvFile:
                    pass
