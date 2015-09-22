UVEX Quicklook JPGs
===================

This directory contains single-band (grayscale) and multi-band (color) JPGs
of all the fields that have been observed as part of the UVEX survey.


Filenames
---------
The JPG filenames are of the form

    YYYYMMDD-HHMM-RUN-FIELD-BAND-small.jpg
    (e.g. 20080822-2157-633779-5032o-col-small.jpg)

where the timestamp refers to the end of the r-band exposure,
RUN refers to the r-band run number, FIELD is the field identifier,
and BAND is one of "u", "g", "r" or "col".  The latter is a color mosaic
where u=blue, g=green, r=red.


Contrast stretching
-------------------
The grayscale levels shown in the JPGs do not scale linearly with the reduced
FITS image pixel data. Instead:
 1) The pixel values have been clipped and normalized to the [25%, 99%]
 interval, i.e. pixel values below the 25% histogram percentile are shown
 in black, and pixel values brighter than the 99% percentile are white.
 2) A *logarithmic* stretching function was applied to the image, bringing
 out faint details near the noise limit.

This contrast stretching strategy was chosen because it worked well for most
IPHAS fields. Note however that very sparse fields will naturally tend to show
more noisy patterns as a result of more background pixels (i.e. pixel
values dominated by read noise) being contained in the [25%, 99%] interval.
Crowded or nebulous fields will naturally show less noise in this scheme.

Although it is common to see noisy patterns in sparse fields for the reasons
described above, such noise is often at the level of a few pixel counts and 
1) may be dealt with by the local background subtraction during photometry,
and 2) is often smaller than other systematics (e.g. atmospheric transparency
changes).  To understand whether noise patterns are important, it is necessary
to open FITS file and determine whether the noise structure exceeds e.g. 3-5%
the background level.


Index of fields
---------------
The FITS table `uvex-casu-dqc-by-field.fits` details all the attempts to
observe UVEX fields, based on the QC information obtained from CASU.
A quicklook JPG was generated for each entry of this table, even those
observing attempts which were very poor (e.g. poor seeing). 
The table is useful for managing quality control and has been copied to this
directory.


Geert Barentsen, 21 Sep 2015.
