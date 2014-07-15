#!/usr/bin/env python
"""Downloads the INT observing logs between 2003 and today."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

__author__ = "Geert Barentsen"

import logging
logging.basicConfig()
log = logging.getLogger()
import mechanize
import datetime
import time


DESTINATION = 'downloaded'  # Where to store the downloaded logs?


def fetch_log(date):
    """Returns the log for a given date as a string."""
    log.info('Fetching the log for {0}'.format(date))
    br = mechanize.Browser()
    br.open("http://www.ing.iac.es/astronomy/observing/inglogs.php")
    br.select_form(nr=1)
    br["form[tel]"] = ["int"]
    br["form[day]"] = ["%02i" % date.day]
    br["form[month]"] = ["%02i" % date.month]
    br["form[year]"] = ["%s" % date.year]
    response = br.submit(nr=1)
    return response.get_data()

def download_log(date):
    """Writes the log for a given date to disk.""" 
    f = open("{0}/intlog_{1:04d}{2:02d}{3:02d}.txt".format(
             DESTINATION, date.year, date.month, date.day),
             'w')
    f.write(fetch_log(date))
    f.close()

def download_all(start_date=datetime.datetime(2003, 1, 1)):
    """Downloads all logs from a given starting date."""
    date = start_date
    today = datetime.datetime.now()
    while date < today:
        download_log(date)
        date += datetime.timedelta(days=1)
        time.sleep(1)  # Let's be nice  


if __name__ == '__main__':
    log.setLevel(logging.INFO)
    download_all(datetime.datetime(2011, 8, 30))
    #download_log(datetime.datetime(2011, 8, 30))