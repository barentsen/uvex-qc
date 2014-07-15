#!/bin/bash

stilts tcat in=uvex-casu-dqc.csv ifmt=csv \
ocmd="addcol -before run runno parseInt(substring(run,1))" \
ofmt=fits out=uvex-casu-dqc.fits

gzip uvex-casu-dqc.fits
