#!/usr/bin/env python2.7
# Start server within an infinite loop: while true; do python2.7 manage.py runserver ; sleep 1; done

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spam05_api.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
