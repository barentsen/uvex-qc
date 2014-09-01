#!/usr/bin/env python
"""Parses the INT observing logs and stores the useful data into CSV tables.

Output
------
This script will create two files:
* logs_bynight.csv : observing conditions, one row per night.
* logs_byrun.csv : pointing details, one row per telescope exposure.

Caveats
-------
* Observers occasionally forget to create the observing log, hence any
database extracted from the observing logs is never complete.
* The INT's instrument control system occasionally fails to write the
coordinates of an exposure to the log, for dark reasons.
* The INT/WFC exposure times recorded in the logs and the FITS headers
are sometimes wrong by an unknown amount. (Which makes life fun.)
"""

__author__ = "Geert Barentsen"

import re
import numpy as np
import os


if __name__ == '__main__':

    csv_bynight = open("intlogs-by-night.csv", "w")
    csv_byrun = open("intlogs-by-run.csv", "w")

    # CSV headers
    csv_bynight.write("night,observer,temp_avg,hum_avg,lost_weather,lost_technical,lost_other,comments_weather,comments_night\n")
    csv_byrun.write("run,name,ra_hms,dec_dms,exptime,night,observer,temp_avg,hum_avg,lost_weather,lost_technical,lost_other,comments_weather,comments_night,comments_exposure\n")


    for filename in sorted(os.listdir("downloaded")):
        if not re.match("intlog_\d+.txt", filename):
            continue

        f = open("downloaded/"+filename, "r")
        log = f.readlines()

        temp, hum = [], []

        # Assume headers take no more than 70 lines
        for i, line in enumerate(log[0:70]):
            m = re.match("^DATE\s*(\d+)", line, re.M|re.S)
            if m: night = m.group(1)

            m = re.match("^OBSERVER/S\s*(.*)\s+$", line, re.M|re.S)
            if m: observer = m.group(1).replace('"', '""')

            m = re.match("^\d{2}:00\s+([0-9.]+)\s+([0-9.]+)", line, re.M|re.S)
            if m: 
                temp.append( m.group(1) )
                hum.append( m.group(2) )

            m = re.match("^TIME LOST weather\s+(\d+:\d+)", line, re.M|re.S)
            if m: lost_weather = m.group(1)

            m = re.match("^TIME LOST Technical\s+(\d+:\d+)", line, re.M|re.S)
            if m: lost_technical = m.group(1)

            m = re.match("^TIME LOST Other\s+(\d+:\d+)", line, re.M|re.S)
            if m: lost_other = m.group(1)

            m = re.match("^WEATHER CONDITIONS(.*)", line, re.M|re.S)
            if m: weather = log[i+1].strip().replace('"', '""')

            m = re.match("^COMMENTS(.*)", line, re.M|re.S)
            if m: night_comments = log[i+1].strip().replace('"', '""')



        out = "%s,\"%s\",%.1f,%.1f,%s,%s,%s,\"%s\",\"%s\"\n" % \
                (night, observer, \
                np.mean(np.array(temp, dtype="float")), \
                np.mean(np.array(hum, dtype="float")), \
                lost_weather, lost_technical, lost_other,
                weather, night_comments)
        csv_bynight.write(out)


        # Data
        for line in log[20:]:

            m = re.match("^\s*(\d\d\d\d\d+).*WFC", line, re.M|re.S)
            if m:
                run = m.group(1).strip()
                name = line[8:25].strip().lower()
                ra = line[25:36].strip()
                dec = line[37:48].strip()
                exptime = line[75:82].strip()
                comments = line[121:].strip().replace('"', '""')


                out = "%s,\"%s\",%s,%s,%s,%s,\"%s\",%.1f,%.1f,%s,%s,%s,\"%s\",\"%s\",\"%s\"\n" % \
                        (run, name, ra, dec, exptime, \
                        night, observer, \
                        np.mean(np.array(temp, dtype="float")), \
                        np.mean(np.array(hum, dtype="float")), \
                        lost_weather, lost_technical, lost_other,
                        weather, night_comments, comments)
                csv_byrun.write(out)

        csv_bynight.flush()
        csv_byrun.flush()


    csv_bynight.close()
    csv_byrun.close()