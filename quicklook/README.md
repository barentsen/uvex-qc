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
The grayscale levels shown in the JPG do not scale linearly with the original
FITS image data. Instead:
 1) The pixel values have been clipped and normalized to the [25%, 99%]
 percentile interval, i.e. pixel values below the 25% histogram percentile
 are shown as black, and pixel values brighter than the 99% percentile are
 shown as white.
 2) A *logarithmic* stretching function was applied to the image, bringing
 out faint details near the noise limit.

This contrast stretching strategy was chosen because it works well for most
images. Note however that very sparse fields will naturally tend to show
more noise as a result of more background pixels falling in the [25%, 99%]
interval, while crowded or nebulous fields will show less noise.


Geert Barentsen, 21 Sep 2015.
