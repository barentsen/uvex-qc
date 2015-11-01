#!/bin/bash

# This script will run through the UVEX files and concatenate all 
# the summary.list files into a single "list.concatenated" file

OUTPUT="tmp/concatenated-summary-list.txt"

# Now copy the contents of all summary.sum8 files, except the header line
for FILE in `find downloaded/ -name "summary.list"`; do
	echo "Adding $FILE"
	cat $FILE >> $OUTPUT
done
