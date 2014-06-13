from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from csv import Sniffer
from csv import Dialect
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
                help='A file that maps the website sensor names to CSV column names.  This file will be structured like '),

            make_option('--fieldnames',
                action='store',
                dest='fieldnames',
                default='',
                help='A list of sensor names (must match website sensor names) seperated by comas in the order of CSV file colomns.  Specify sensor data value type like .avg or .max; Can be one of .avg, .min, .max, .std, .total (e.g. sensor1.avg,sensor1.total,sensor2.avg )'),

            make_option('--fieldnames-file',
                action='store',
                dest='fieldnames-file',
                default='',
                help='Load the sensor names from a file.  The sensor names should be formatted like the --fieldnames option'),

            make_option('--force-has-header',
                action='store-True',
                dest'force-header',
                default=False
                help='Forces the first line of the CSV file to be read as the header containing sensor names.  Normally the CSV file is checked for a first line header.  Use this option if the CSV first line header is not being detected properly'),

            make_option('--skip',
                action='store',
                dest='skip',
                type='int',
                default=0,
                help='Skip n number of lines before reading CSV file'),
        )

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError('Must only have 2 argurments (station_name and filename)')

        if options['fieldnames']:
            colNames = options['fieldnames'].split()
        elif options['fieldnames-file']:
            with open(options['fieldnames-file']) as f:
                colNames = f.next().split()

        maping = None
        if options['mapfile']:
            with open(options['mapfile']) as f:
                buf = f.read()
                maping = buf.split('\n,')

        with open(args[1],'r') as f:
            #detect position of first character for starting line (default: 0)
            firstChar = 0
            if options['skip'] > 0:
                for n in range(options['skip']):
                    f.next()
                firstChar = f.tell()

            #decide whether or not to read the first line as header
            has_header = False
            if options['force-header']:
                has_header = True
            else
                #read first 1000 characters to auto-detect the presence of a header
                has_header = Sniffer().has_header(f.read(1000))
                f.seek(firstChar)

            #auto detect CSV dialect
            d = Sniffer().sniff(f.read(1000))
            f.seek(firstChar)

            if has_header:
                reader = DictReader(f, dialect=d)
                #copy detected field names from Dictionary Reader
                colNames = reader.fieldnames
            else
                reader = DictReader(f, fieldnames=colNames, dialect=d)
            for row in reader:
                    pass
