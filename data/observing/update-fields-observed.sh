#!/bin/bash
# Creates a list of unique fields observed recently
#grep uvex seeing-logs/seeing_* | awk '{ print $10 }' | sed s/'uvex_'/''/g | sort | uniq > fields-observed-in-2014.txt 
python parse-seeing-logs.py
