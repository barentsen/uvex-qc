#!/bin/bash
stilts tcat in=tmp/uvex-casu-dqc-by-run.csv ifmt=csv \
ocmd="addcol -before run runno parseInt(substring(run,1));
      addcol -before ra_hms ra hmsToDegrees(ra_hms);
      addcol -before ra_hms dec dmsToDegrees(dec_dms);
      replacecol name 'name.toLowerCase()';
      addskycoords -inunit deg -outunit deg icrs galactic ra dec l b;
      select 'name.startsWith(\"uvex\")';
      addcol field 'trim(name.split(\"_\")[1].split(\" \")[0])';" \
ofmt=fits out=uvex-casu-dqc-by-run.fits
#gzip uvex-casu-dqc.fits

# replacecol seeing parseFloat(seeing);
# replacecol sky parseFloat(sky);
# replacecol ellipt parseFloat(ellipt);