"""
Create quicklook JPEGs for UVEX/IPHAS quality control.

This script will create the JPEGs using the following typical command sequence:
funpack r564465.fit.fz
mosaic r564465.fit Ha_conf.fits hamos.fit hamosconf.fit --skyflag=0 --verbose
mJPEG -gray hamos.fit 20% 99.9% log -out hamos.jpg
mJPEG -gray rmos.fit 20% 99.9% log -out rmos.jpg
mJPEG -gray imos.fit 20% 99.9% log -out imos.jpg
convert hamos.jpg rmos.jpg imos.jpg -set colorspace RGB -combine -set colorspace sRGB rgbmos.jpg

To convert the result into a silly movie, use
ffmpeg -f image2 -pattern_type glob -r 4 -i 'iphas-quicklook/*small.jpg' -c:v libx264 iphas.avi
or given a list of images
cat $(cat list.txt) | ffmpeg -r 4 -f image2pipe -vcodec mjpeg -i - -c:v libx264 iphas.avi
"""

import os
import subprocess
import shlex
import glob

from astropy import log
import astropy.io import fits
from astropy.table import Table


""" CONFIGURATION CONSTANTS """
RUN2PATH = json.load(open("/home/gb/dev/uvex-qc/data/image-index/run2path.json"))
DIR2CONF = json.load(open("/home/gb/dev/uvex-qc/data/image-index/dir2conf.json"))

OUTPATH = '/car-data/gb/uvex-quicklook'
DATADIR = '/car-data/gb/iphas'
WORKDIR = '/tmp/gb-scratch'

BANDS = ['u', 'g', 'r']
MOSAIC = '/home/gb/bin/casutools/bin/mosaic'
FPACK = '/home/gb/bin/cfitsio3310/bin/fpack'
FUNPACK = '/home/gb/bin/cfitsio3310/bin/funpack'
MJPEG = '/soft/Montage_v3.3/bin/mJPEG'
MSHRINK = '/soft/Montage_v3.3/bin/mShrink'
CONVERT = '/usr/bin/convert'


class Quicklook():
    """ 
    Computes quicklook jpegs for a given field.

    Parameters
    ----------
    run_u, run_g, run_r : str, str, str
        Run numbers

    time_r : str
        Timestamp.

    fieldid : str
        Field identifier, e.g. '0009o'.
    """

    def __init__(self, run_u, run_g, run_r, time_r, fieldid):
        self.run_u, self.run_g, self.run_r = str(run_u), str(run_g), str(run_r)
        self.time_r = time_r
        self.fieldid = fieldid
        
        self.workdir = WORKDIR
        timestamp = self.time_r[0:16].replace('-', '').replace(':', '').replace(' ', '-')
        self.filename_root = os.path.join(self.workdir,
                                          self.run_r +
                                          "-" + timestamp + 
                                          "-" + self.fieldid)
        self.files_to_remove = []

    def get_fits_filenames(self):
        """
        Returns the location of the three images which make up a field,
        and raises an exception if they cannot be found on the filesystem.

        """
        result = {'img_u': RUN2PATH[self.run_u],
                  'img_g': RUN2PATH[self.run_g],
                  'img_r': RUN2PATH[self.run_r]}
        # Test if all the files exist
        for key in result.keys():
            if not os.path.exists( result[key] ):
                raise Exception('Field %s: file %s does not exist' % (
                        self.run_r,
                        result[key]) )
        return result

    def execute(self, cmd):
        """Executes a shell command and logs any errors."""
        log.debug(cmd)
        p = subprocess.Popen(shlex.split(cmd), 
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout = p.stdout.read().strip()
        stderr = p.stderr.read().strip()
        if stderr:
            raise Exception("Error detected in quicklook.execute: "
                            "STDERR={%s} STDOUT={%s} CMD={%s}" % (
                                stderr, stdout, cmd))
        if stdout:
            log.debug( stdout )
        return True

    def setup_workdir(self):
        """Setup the working directory for storing tmp files."""
        if not os.path.exists(self.workdir):
            self.execute('mkdir %s' % self.workdir)

    def move_jpegs(self):
        """Move the output jpegs to the final destination."""
        files_to_move = [ self.filename_root + '.jpg',
                          self.filename_root + '_small.jpg' ]
        for band in BANDS:
            files_to_move.append(self.filename_root + '_' + band + '.jpg' )
            files_to_move.append(self.filename_root + '_small_' + band + '.jpg' )
            files_to_move.append(self.filename_root + '_' + band + '.fit')

        for filename in files_to_move:
            cmd = '/bin/mv %s %s' % (
                    filename,
                    OUTPATH)
            self.execute(cmd)

    def clean_workdir(self):
        """Removes temporary files from the working directory."""
        #files_to_remove = []
        #for filename in glob.iglob(self.workdir + '/*' + self.fieldid + '*'):
        #    files_to_remove.append(filename)

        # Delete the leftover fits files
        for filename in self.files_to_remove:
            cmd = '/bin/chmod +w %s' % filename
            self.execute(cmd)
            cmd = '/bin/rm %s' % filename
            self.execute(cmd)
            
    def compute_jpegs(self):
        assert( os.path.exists(self.workdir) )
        fits_filenames = self.get_fits_filenames()
        
        for band in BANDS:
            filename_fits = self.filename_root + '_' + band + '.fit'
            filename_conf = self.filename_root + '_' + band + '_conf.fit'
            filename_jpg = self.filename_root + '_' + band + '.jpg'
            filename_jpg_small = self.filename_root + '_small_' + band + '.jpg'     

            # CASUTools/Mosaic
            cmd = '%s %s %s %s %s --skyflag=0' % (
                MOSAIC,
                fits_filenames['img_' + band],
                CONF[band],
                filename_fits,
                filename_conf )
            self.execute(cmd)
            self.files_to_remove.append(filename_conf)

            # Montage requires the equinox keyword to be '2000.0'
            # but CASUtools sets the value 'J2000.0'
            myfits = fits.open(filename_fits)
            myfits[0].header.update('EQUINOX', '2000.0')
            myfits.writeto(filename_fits, clobber=True)

            # Montage/mJPEG
            cmd = '%s -gray %s 25%% 99.9%% log -out %s' % (
                    MJPEG,
                    filename_fits,
                    filename_jpg )
            self.execute(cmd)

            # Make a smaller version, too
            cmd = '%s %s -resize 600 -quality 70 %s' % (
                    CONVERT,
                    filename_jpg,
                    filename_jpg_small )
            self.execute(cmd)

            """
            # Compress the mosaicked FITS file
            cmd = '%s -D -Y %s' % (
                    FPACK,
                    filename_fits )
            self.execute(cmd)
            """

            # Shrink the mosaicked FITS file
            cmd = '%s %s %s 6' % (
                    MSHRINK,
                    filename_fits,
                    filename_fits )
            self.execute(cmd)
            

        # Final color mosaic
        # We have to ensure that the channels have the same number of pixels
        cmd = '%s %s %s %s -set colorspace RGB -combine -set colorspace sRGB %s' % (
                CONVERT,
                self.filename_root + '_r.jpg[6210x6145+0+0]',
                self.filename_root + '_g.jpg[6210x6145+0+0]', 
                self.filename_root + '_u.jpg[6210x6145+0+0]', 
                self.filename_root + '.jpg'
                )
        self.execute(cmd)

        # Small version
        cmd = '%s %s -resize 600 -quality 70 %s' % (
                CONVERT,
                self.filename_root + '.jpg',
                self.filename_root + '_small.jpg')
        self.execute(cmd)

    def run(self):
        """Main execution loop
        """
        try:
            self.setup_workdir()
            self.compute_jpegs()
            self.move_jpegs()
            self.clean_workdir()
            return True
        except Exception, e:
            log.error('Quicklook.run() aborted with exception: "%s"' % e)
            #self.clean_workdir()
            return False


if __name__ == '__main__':
    t = Table.read('/home/gb/dev/uvex-qc/data/casu-dqc/uvex-casu-dqc-by-field.fits')
    mask = (field['runno_u'] != '') & (field['runno_g'] != '') & (field['runno_r'] != '')
    for field in t[mask][0:2]:
        ql = Quicklook(field['runno_u'], field['runno_g'], field['runno_r'],
                       field['time_r'], field['field'])
        ql.run()
