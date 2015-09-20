"""Create a JSON file that maps run numbers onto file system paths."""
import os
import re
import json

import numpy as np
from astropy import log


OUTPUT_FN = "run2path.json"

DIRS_TO_IGNORE = ['junk', 'badones', 'crap', '9thoct', \
                  'Uband', 'gband', 'PROBLEMS']

if __name__ == "__main__":
    output = {}

    with open("egaps-fits-files.csv", "r") as egapsfiles:
        for entry in egapsfiles:
            path = entry.strip()
            # Some directories are ment to be disregarded
            if np.any([d in path for d in DIRS_TO_IGNORE]):
                continue
            filename = os.path.basename(path)
            if re.match('^r\d+.fit', filename):
                runno = filename.split('.')[0][1:]
                #if runno in output:
                #    log.warning("{}: duplicate:\n{}\n{}\n".format(runno, path, output[runno]))
                output[runno] = path

    log.info("Writing {}".format(OUTPUT_FN))
    json.dump(output, open(OUTPUT_FN, "w"), indent=2)
