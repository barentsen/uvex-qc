"""Make a list of all the FITS files in the IPHAS/UVEX reduced data from CASU.

The output is a CSV table with paths to the fits files.
"""
import os
from astropy import log

# Config
DATADIR = '/car-data/gb/iphas/'


if __name__ == "__main__":
    out = open('egaps-fits-files.csv', 'w')
    for mydir in os.walk(DATADIR, followlinks=True):
        log.info('Entering '+mydir[0])
        for filename in mydir[2]:
            if filename.endswith("fit") or filename.endswith("fits"):
                out.write("{}\n".format(os.path.join(mydir[0], filename))) 
        out.flush()
    out.close()
