import numpy as np

from astropy.table import Table

if __name__ == "__main__":
    t = Table.read('/home/gb/dev/uvex-qc/data/casu-dqc/uvex-casu-dqc-by-field.fits')
    for dirname in np.unique(t["dir"]):
        cmd = 'qsub -v DIRNAME={} -N uvex_ql_{} quicklook.pbs'.format(
                    dirname, dirname)
        print(cmd)