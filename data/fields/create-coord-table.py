#!/usr/bin/env python
"""Creates a user-friendly table with IPHAS/UVEX field coordinates."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np
from astropy.table import Table
from astropy.coordinates import SkyCoord

fields = []
def add_field(name, ra, dec):
    fields.append([name, ra, dec])

if __name__ == '__main__':
    col_name, col_ra, col_dec = [], [], []
    fivearcmin = 5./60.
    t = Table.read('iphas-planner.fits')
    for i, name in enumerate(t['name']):
        myname = name.split('_')[1]
        col_name.append(myname)
        col_ra.append(t[i]['ra'])
        col_dec.append(t[i]['dec'])
        col_name.append(myname+'o')
        col_ra.append(t[i]['ra'] + (fivearcmin/np.cos(np.radians(t[i]['dec']))))
        col_dec.append(t[i]['dec'] + fivearcmin)

    col_name, col_ra, col_dec = np.array(col_name), np.array(col_ra), np.array(col_dec)
    gal = SkyCoord(col_ra, col_dec, unit='deg').galactic

    newtable = Table([col_name, col_ra, col_dec, gal.l.value, gal.b.value],
                     names=['field', 'ra', 'dec', 'l', 'b'])
    newtable.write('field-coordinates.fits', overwrite=True)