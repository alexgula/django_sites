from json import dumps
from django.core.management.base import BaseCommand, CommandError
from ...util import color_map

class Command(BaseCommand):
    args = '<source_file_name> <destination_file_name>'
    help = 'Analyze color map from file and generate JSON array.'

    def handle(self, src_file_name, dest_file_name, *args, **options):
        data = color_map.build_color_data(src_file_name)
        sdata = dumps(data)
        with open(dest_file_name, 'w') as file:
            file.write("region_map=")
            file.write(sdata)
        self.stdout.write('Successfully loaded file "{}"\n'.format(src_file_name))
        self.stdout.write('Successfully saved file "{}"\n'.format(dest_file_name))
