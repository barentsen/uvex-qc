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

# Which uvex fields have been observed at least ones?
UVEX_ATTEMPTED = read_fieldlist('../data/casu-dqc/reduced-uvex-fields.txt')
# Which of the reduced fields failed QC? (List provided by Paul Groot.)
UVEX_FAILED = read_fieldlist('../data/casu-dqc/reduced-uvex-fields-which-may-be-good.txt')


if __name__ == '__main__':
    TODO_A, TODO_B = [], []
    for i in np.arange(1, 7635+1, 1):
        for field in ['{0:04d}'.format(i), '{0:04d}o'.format(i)]:
            if field not in UVEX_ATTEMPTED:
                TODO_A.append(field)
            elif field in UVEX_FAILED:
                TODO_B.append(field)

    print('{} fields observed, {} failed QC.'.format(len(UVEX_ATTEMPTED),
                                                     len(UVEX_FAILED)))
    print('{0} fields left to do: {1} never attempted, {2} failed.'.format(
            len(TODO_A)+len(TODO_B), len(TODO_A), len(TODO_B)))

    with open('uvex-fields-never-attempted.txt', 'w') as output:
        for field in TODO_A:
            output.write(field+'\n')
        print("Writing {}".format(output.name))
        output.close()
    with open('uvex-fields-failed.txt', 'w') as output:
        for field in TODO_B:
            output.write(field+'\n')
        print("Writing {}".format(output.name))
        output.close()
