# coding=utf-8
"""Simple HTTP ping using Requests library"""

import datetime
import time
import requests

def iterping(url, sleep):
    """Infinite generator for pinging given url with given period."""
    while True:
        start = datetime.datetime.now()
        status = requests.get(url).status_code
        end = datetime.datetime.now()
        yield status, start, end
        time.sleep(sleep)

def formatping(status, start, end):
    """Simple example of formatting ping messages."""
    return "{}: got {} in {} sec".format(start, status, end - start)

def iterprint(url, sleep, formatter=formatping):
    """Simple wrapper for printing pings."""
    for result in iterping(url, sleep):
        print(formatter(*result))
