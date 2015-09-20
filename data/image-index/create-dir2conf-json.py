"""Creates a JSON file mapping directories onto confidence maps."""
import os
import json

from astropy import log


OUTPUT_FN = "dir2conf.json"


if __name__ == "__main__":
    output = {}

    with open("egaps-fits-files.csv") as fitsfiles:
        for entry in fitsfiles:
            # Is it a confidence map?
            if "cpm" in entry or "conf" in entry:
                path = entry.strip()
                mydir = os.path.dirname(path)
                if not mydir in output:
                    output[mydir] = {}

                filename = os.path.basename(path)
                if filename.lower().startswith("u"):
                    output[mydir]['u'] = path
                if filename.lower().startswith("g"):
                    output[mydir]['g'] = path
                if filename.startswith("r"): 
                    output[mydir]['r'] = path
                elif filename.startswith("i"): 
                    output[mydir]['i'] = path
                elif filename.lower().startswith("ha") or filename.startswith("h_"):
                    output[mydir]['ha'] = path 

    log.info("Writing {}".format(OUTPUT_FN))
    json.dump(output, open(OUTPUT_FN, "w"), indent=2)

