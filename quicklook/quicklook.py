"""
Converts all IPHAS science images to four JPEGs (one per CCD) using 
Montage/mJPEG

Typical command sequence:
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
import astropy.io.fits as pyfits
from astropy.table import Table
import logging
import subprocess
import shlex
import glob

""" CONFIGURATION CONSTANTS """
BANDS = ['u', 'g', 'r']
DATADIR = '/car-data/gb/iphas'
MOSAIC = '/home/gb/bin/casutools/bin/mosaic'
FPACK = '/home/gb/bin/cfitsio3310/bin/fpack'
FUNPACK = '/home/gb/bin/cfitsio3310/bin/funpack'
MJPEG = '/local/home/gb/bin/Montage_v3.3/mJPEG'
MSHRINK = '/local/home/gb/bin/Montage_v3.3/mShrink'
CONVERT = '/usr/bin/convert'

CONF = {'u':'/home/gb/tmp/uvexdata/uvex_sep2007/U_conf.fit',
        'g':'/home/gb/tmp/uvexdata/uvex_sep2007/g_conf.fit',
        'r':'/home/gb/tmp/uvexdata/uvex_sep2007/r_conf.fit'}


if os.uname()[1] == 'xps': 
    # Local
    DATADIR = '/home/gb/tmp/uvexdata'
    MOSAIC = '/home/gb/bin/bin/bin/mosaic'
    FPACK = '/home/gb/bin/bin/bin/fpack'
    FUNPACK = '/home/gb/bin/bin/bin/funpack'
    MJPEG = '/home/gb/bin/bin/bin/mJPEG'
    MSHRINK = '/home/gb/bin/bin/bin/mShrink'
    OUTPATH = '/home/gb/tmp/uvex-quicklook'
    WORKDIR = '/dev/shm'
else: 
    # Cluster
    MJPEG = '/soft/Montage_v3.3/bin/mJPEG'
    MSHRINK = '/soft/Montage_v3.3/bin/mShrink'
    OUTPATH = '/car-data/gb/uvex/quicklook'
    WORKDIR = '/tmp/gb-scratch'


class Quicklook():
    """ 
    Computes quicklook jpegs for a given field.

    Parameters
        :fieldid: (required)
        field identifier string, e.g. '0009o_aug2010'

    Usage
        ql = Quicklook('0009o_aug2010')
        ql.run()
    """

    def __init__(self, directory, run_r, run_u, run_g):
        """
        Constructor

        """
        self.directory = directory
        self.run_u, self.run_g, self.run_r = str(run_u), str(run_g), str(run_r)
        self.workdir = WORKDIR
        self.filename_root = self.workdir + '/' + self.run_r
        self.log = logging
        self.files_to_remove = []

    def get_fits_filenames(self):
        """
        Returns the location of the three images which make up a field,
        and raises an exception if they cannot be found on the filesystem.

        """
        result = {'img_u': os.path.join(self.directory, 'r' + self.run_u + '.fit'),
                  'img_g': os.path.join(self.directory, 'r' + self.run_g + '.fit'),
                  'img_r': os.path.join(self.directory, 'r' + self.run_r + '.fit')}
        # Test if all the files exist
        for key in result.keys():
            if not os.path.exists( result[key] ):
                raise Exception('Field %s: file %s does not exist' % (
                        self.run_r,
                        result[key]) )
        return result

    def execute(self, cmd):
        """
        Executes a shell command and logs any errors.

        """
        self.log.debug(cmd)
        p = subprocess.Popen(shlex.split(cmd), 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = p.stdout.read().strip()
        stderr = p.stderr.read().strip()
        if stderr:
            raise Exception("Error detected in quicklook.execute: STDERR={%s} STDOUT={%s} CMD={%s}" % (
                                stderr, stdout, cmd))
        if stdout:
            self.log.debug( stdout )
        return True

    def setup_workdir(self):
        """
        Setup the working directory.

        """
        if not os.path.exists(self.workdir):
            self.execute('mkdir %s' % self.workdir)

    def move_jpegs(self):
        """
        Move the resulting jpegs to their desired location.

        """
        files_to_move = [ self.filename_root + '.jpg',
                          self.filename_root + '_small.jpg' ]
        for band in BANDS:
            files_to_move.append(self.filename_root + '_' + band + '.jpg' )
            files_to_move.append(self.filename_root + '_small_' + band + '.jpg' )
            files_to_move.append(self.filename_root + '_' + band + '.fit')

        for filename in files_to_move:
            cmd = '/bin/mv %s %s' % (
                    filename,
                    OUTPATH )
            self.execute(cmd)

    def clean_workdir(self):
        """
        Clean the working directory.

        """
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
            myfits = pyfits.open(filename_fits)
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
        """
        Main execution loop

        """
        try:
            self.setup_workdir()
            self.compute_jpegs()
            self.move_jpegs()
            self.clean_workdir()
            return True
        except Exception, e:
            self.log.error('Quicklook.run() aborted with exception: "%s"' % e)
            #self.clean_workdir()
            return False



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, 
    format="%(asctime)s/%(levelname)s: %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S" )

    t = Table.read('/home/gb/dev/uvex-qc/data/casu-dqc/uvex-casu-dqc-by-field.fits')
    for field in t:
        if (field['runno_u'] != '') and (field['runno_g'] != '') and (field['runno_r'] != ''):
            mydir = os.path.join(DATADIR, field['dir'])
            ql = Quicklook(mydir, field['runno_r'], field['runno_u'], field['runno_g'])
            ql.run()

    #quicklook = Quicklook('/home/gb/tmp/uvexdata/uvex_sep2007', 583191, 583192, 583193)
    #quicklook = Quicklook('/home/gb/tmp/uvexdata/uvex_sep2007', 583127, 583128, 583129)
    #quicklook.run()
