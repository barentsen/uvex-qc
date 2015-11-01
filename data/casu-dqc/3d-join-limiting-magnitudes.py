import numpy as np
from astropy.table import Table, join

t1 = Table.read("tmp/uvex-casu-dqc-by-run.csv")
t2 = Table.read("tmp/limiting-mags.csv")
# The summary.list files list each CCD individually, so let's group
tnew = t2.group_by("run").groups.aggregate(np.mean)
result = join(t1, tnew, join_type="left")
result.write("tmp/uvex-casu-dqc-by-run-with-lm.csv")
