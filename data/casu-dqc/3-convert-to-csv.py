#!/usr/bin/env python
from astropy.io import ascii

# Dirty hack: there are two different fixed-width formats at play :-(
# we cope with this by removing 2 characters from one of the alternatives,
# bringing the format in line with the other.
with open('tmp/uvex-casu-dqc.txt.corrected', 'w') as output, open("tmp/uvex-casu-dqc.txt", 'r') as original:
    for line in original.readlines():
        if len(line) == 175:
            output.write(line[:127]+line[129:])
        else:
            output.write(line)

# Convert the fixed-width concatenated sum8 files to CSV
data = ascii.read("tmp/uvex-casu-dqc.txt.corrected", data_start=1, \
					Reader=ascii.FixedWidthNoHeader, 
					names=('dir', 'run', 'name', 'ra_hms', 'dec_dms', 'airmass', 'posang', 'time', 'exptime', 'filter', 'seeing', 'sky', 'noise', 'ellipt', 'apcor', 'comments'), \
					col_starts=(0, 0+16, 16+16, 34+16, 46+16, 64+16, 70+16, 76+16, 98+16, 107+16, 111+16, 116+16, 124+16, 130+16, 136+16, 142+16), \
					col_ends=(14, 14+16, 32+16, 44+16, 56+16, 68+16, 74+16, 96+16, 104+16, 109+16, 114+16, 122+16, 128+16, 134+16, 140+16, 157+16))
ascii.write(data, output="tmp/uvex-casu-dqc-by-run.csv", delimiter=",")