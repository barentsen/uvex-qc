"""Check to see if the JSON files contain all the info we need."""
import os
import json
import numpy as np

from astropy.table import Table
from astropy import log


RUN2PATH = json.load(open("run2path.json", "r"))
DIR2CONF = json.load(open("dir2conf.json", "r"))

BANDS = ["u", "g", "r"]

if __name__ == "__main__":
    qc = Table.read("/home/gb/dev/uvex-qc/data/casu-dqc/uvex-casu-dqc-by-field.fits")
    for row in qc:
        if np.all([row["runno_"+band] != "" for band in BANDS]):
            for band in ["u", "g", "r"]:
                runno = row["runno_"+band]

                # Check if we have the image FITS file for the run number
                if not runno in RUN2PATH:
                    log.error("{}: image missing".format(runno))
                else:
                    # Check if we know the confidence map for this directory
                    directory = os.path.dirname(RUN2PATH[runno])
                    if directory not in DIR2CONF or band not in DIR2CONF[directory]:
                        log.error("{}: {} conf map missing".format(directory, band))
