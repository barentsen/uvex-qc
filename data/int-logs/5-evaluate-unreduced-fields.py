#!/usr/bin/env python
"""Identify which of the unreduced fields are potentially good.

This script produces `unreduced-uvex-fields-which-may-be-good.txt`.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import numpy as np
from astropy.table import Table

# Nights with no hope of useful data, judging by the logs:
HORRENDOUS_NIGHTS = [20060722, 20101103, 20110729, 20111124, 20111125]

t = Table.read('uvex-unreduced-fields.fits')


if __name__ == '__main__':
    # Assume we only care about U, g and r
    goodfields = []
    for i in np.argsort(t['field']):
        if (t[i]['run_u'] != '' and t[i]['run_g'] != '' and t[i]['run_r'] != ''
            and t[i]['night'] not in HORRENDOUS_NIGHTS):
            goodfields.append(t[i]['field'])
    print('Found {0} potentially good fields which have not been reduced yet.'.format(np.unique(goodfields).size))
    with open('unreduced-uvex-fields-which-may-be-good.txt', 'w') as output:
        for field in np.unique(goodfields):
            output.write(field+'\n')

    # By-product: list of fields attempted
    t = Table.read('uvex-logs-by-run.fits')
    with open('uvex-fields-attempted.txt', 'w') as output:
        for field in np.sort(np.unique(t['field'])):
            output.write(field+'\n')
