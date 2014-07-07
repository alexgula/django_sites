from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import activate
from ...data_import import load

class Command(BaseCommand):
    args = '<file_name>'
    help = 'Load data from XML file from 1C.'

    def handle(self, file_name, *args, **options):
        activate('uk')
        load(file_name)
        self.stdout.write('Successfully loaded file "{}"\n'.format(file_name))
