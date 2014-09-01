#!/bin/bash
stilts tcat in=intlogs-by-run.csv ifmt=csv \
ocmd="addcol -before ra_hms ra hmsToDegrees(ra_hms);
      addcol -before ra_hms dec dmsToDegrees(dec_dms);
      addskycoords -inunit deg -outunit deg icrs galactic ra dec l b;
      addcol filter 'trim(name.split(\" \")[1])';
      addcol field 'trim(name.split(\"_\")[1].split(\" \")[0])';" \
ofmt=fits out=int-logs-by-run.fits

# Create a file with uvex runs only
stilts tcat in=int-logs-by-run.fits ifmt=fits \
ocmd="select 'name.startsWith(\"uvex_\")';" \
ofmt=fits out=uvex-logs-by-run.fits

# Create a file with iphas runs only
stilts tcat in=int-logs-by-run.fits ifmt=fits \
ocmd="select 'name.startsWith(\"intphas_\")';" \
ofmt=fits out=iphas-logs-by-run.fits

# Create a file with kepler runs only
stilts tcat in=int-logs-by-run.fits ifmt=fits \
ocmd="select 'name.startsWith(\"kepler_\")';" \
ofmt=fits out=kepler-logs-by-run.fits

# Identify uvex runs thats have not been reduced yet
stilts tmatch2 \
in1=uvex-logs-by-run.fits in2=../casu-dqc/uvex-casu-dqc-by-run.fits \
values1=run values2=runno join=1not2 matcher=exact \
ofmt=fits out=uvex-unreduced-runs.fits

# Compress the results
gzip -f int-logs-by-run.fits uvex-logs-by-run.fits iphas-logs-by-run.fits kepler-logs-by-run.fits