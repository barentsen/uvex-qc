#!/usr/bin/env python
"""Creates UVEX todo files.

We distinguish two categories:
Priority A: fields never attempted before
Priority B: fields attempted before but of poor quality
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np

def read_fieldlist(filename):
    return [field.strip() for field in open(filename).readlines()]

UVEX_ATTEMPTED = read_fieldlist('../data/int-logs/uvex-fields-attempted.txt')
UVEX_OK_REDUCED = read_fieldlist('../data/casu-dqc/reduced-uvex-fields-which-may-be-good.txt')
UVEX_OK_UNREDUCED = read_fieldlist('../data/int-logs/unreduced-uvex-fields-which-may-be-good.txt')
UVEX_OK = np.unique(UVEX_OK_REDUCED + UVEX_OK_UNREDUCED)

if __name__ == '__main__':

    TODO_A, TODO_B = [], []

    for i in np.arange(1, 7635+1, 1):
        for field in ['{0:04d}'.format(i), '{0:04d}o'.format(i)]:
            if field not in UVEX_OK:
                if field not in UVEX_ATTEMPTED:
                    TODO_A.append(field)
                else:
                    TODO_B.append(field)

    print('{0} fields assumed OK ({1} reduced, {2} unreduced).'.format(
          len(UVEX_OK), len(UVEX_OK_REDUCED), len(UVEX_OK_UNREDUCED)))
    print('{0} fields left to do ({1} never attempted, {2} failed).'.format(len(TODO_A)+len(TODO_B), len(TODO_A), len(TODO_B)))

    with open('uvex-fields-never-attempted.txt', 'w') as output:
        for field in TODO_A:
            output.write(field+'\n')
    with open('uvex-fields-failed.txt', 'w') as output:
        for field in TODO_B:
            output.write(field+'\n')