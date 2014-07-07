# coding=utf-8
import logging
from django.core.management.base import BaseCommand
from picassoft.utils.http import post_xml_file


class Command(BaseCommand):
    args = '<site_name> <file_name> <response_file_name>'
    help = 'Upload data from XML file from 1C to site. Saves response html into separate file'

    def handle(self, site_name, file_name, response_file_name, *args, **options):
        r = post_xml_file(site_name + '/interop/upload/', file_name, 'interop', 'nedopaka129')
        with open(response_file_name, 'w') as f:
            f.write(r.content)
        logging.info(
            u'Successfully posted file "{file}" to site {site} (status {status}, see response in {response})'.format(
                file=file_name, site=site_name, status=r.status_code, response=response_file_name))
