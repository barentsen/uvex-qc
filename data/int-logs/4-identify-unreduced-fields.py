#!/usr/bin/env python
"""Identifies unreduced UVEX fields which may be of good quality.

This script produces `uvex-unreduced-fields.fits`.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import numpy as np
from astropy.table import Table

COLNAMES = ('field', 'l', 'b', 'run_u', 'run_g', 'run_r', 'run_he1',
            'night', 'comments_weather', 'comments_night')

fieldlist = []
def register(field):
    # Fill missing values
    for name in COLNAMES:
        if not field.has_key(name):
            if name.startswith(('run')):
                field[name] = ''
            else:
                field[name] = np.float32(np.nan)
    fieldlist.append(field)


if __name__ == '__main__':
    t = Table.read('uvex-unreduced-runs.fits')

    field = {'field': 'ignore'}  # hack: "ignore" the first field

    for idx in np.argsort(t['run']):
        myrun = t[idx]['run']
        myname = t[idx]['name'].strip().split('_')[1].split(' ')[0]
        myfilter = t[idx]['filter'].strip().lower()

        if myfilter not in ['u', 'g', 'r', 'he1']:
            logging.warn('run {0} used filter {1}'.format(myrun, myfilter))
            continue  # ignore run

        if field['field'] != myname:
            if field['field'] != 'ignore':
                register(field)
            field = {'field': myname,
                     'night': t[idx]['night'],
                     'comments_weather': t[idx]['comments_weather'],
                     'comments_night': t[idx]['comments_night'],
                     'l': t[idx]['l'],
                     'b': t[idx]['b']}
        
        for colname in ['run']:
            field[colname+'_'+myfilter] = t[idx][colname]

    Table(fieldlist, names=COLNAMES).write('uvex-unreduced-fields.fits', overwrite=True)
