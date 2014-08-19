#!/bin/bash
stilts tcat in=intlogs-by-run.csv ifmt=csv \
ocmd="addcol -before ra_hms ra hmsToDegrees(ra_hms);
      addcol -before ra_hms dec dmsToDegrees(dec_dms);
      addskycoords -inunit deg -outunit deg icrs galactic ra dec l b;
      select 'name.startsWith(\"uvex_\")';
      addcol filter 'trim(name.split(\" \")[1])';
      addcol field 'trim(name.split(\"_\")[1].split(\" \")[0])';" \
ofmt=fits out=uvex-logs-by-run.fits

# Identify runs thats have not been reduced yet
stilts tmatch2 \
in1=uvex-logs-by-run.fits in2=../casu-dqc/uvex-casu-dqc-by-run.fits \
values1=run values2=runno join=1not2 matcher=exact \
ofmt=fits out=uvex-unreduced-runs.fits