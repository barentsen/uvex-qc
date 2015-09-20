"""Check to see if the JSON files contain all the info we need."""
import os
import json
import numpy as np

from astropy.table import Table
from astropy import log


RUN2PATH = json.load(open("run2path.json", "r"))
COLSTOCHECK = ["runno_u", "runno_g", "runno_r"]

if __name__ == "__main__":
    qc = Table.read("/home/gb/dev/uvex-qc/data/casu-dqc/uvex-casu-dqc-by-field.fits")
    for row in qc:
        # Skip dirs known to be missing
        if row["dir"] in ["jul2013", "dec2011", "nov2012", "dec2012", "dec2012b"]:
            continue

        if np.all([row[col] != "" for col in COLSTOCHECK]):
            for col in COLSTOCHECK:
                if not row[col] in RUN2PATH:
                    log.error("{}".format(row[col]))
