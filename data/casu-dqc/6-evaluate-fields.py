#!/usr/bin/env python
"""Identify which of the reduced fields look good.

This script produces `reduced-uvex-fields-which-may-be-good.txt`.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import numpy as np
from astropy.table import Table

SEEING_LIMIT = 1.7  # arcsec
AIRMASS_LIMIT = 2.0
ELLIPT_LIMIT = 0.3

t = Table.read('uvex-casu-dqc-by-field.fits')

if __name__ == '__main__':
    # First, assume we only care about U/g/r
    goodfields = []
    for i in np.argsort(t['field']):
        if ((t[i]['runno_u'] != ''
            and t[i]['runno_g'] != ''
            and t[i]['runno_r'] != ''
            and t[i]['seeing_g'] < SEEING_LIMIT
            and t[i]['seeing_r'] < SEEING_LIMIT
            and t[i]['ellipt_g'] < ELLIPT_LIMIT
            and t[i]['ellipt_r'] < ELLIPT_LIMIT
            and t[i]['airmass_g'] < AIRMASS_LIMIT
            and t[i]['airmass_r'] < AIRMASS_LIMIT
            ) or (5 < (t[i]['ra']/15.) < 12)):
            goodfields.append(t[i]['field'])

    print('Found {0} potentially good fields.'.format(np.unique(goodfields).size))
    with open('reduced-uvex-fields-which-may-be-good.txt', 'w') as output:
        for field in np.unique(goodfields):
            output.write(field+'\n')
