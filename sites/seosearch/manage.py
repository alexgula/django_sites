#!/usr/bin/env python
import os, sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seosearch.settings")

    from django.core.management import execute_from_command_line

    PORT = '8004'
    args = sys.argv
    if ('runserver' in args or 'runserver_plus' in args) and not PORT in args:
        args.append(PORT)
    execute_from_command_line(args)
