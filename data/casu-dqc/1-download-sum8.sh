#!/bin/bash

# Recursively downloads all *.sum8 files at Cambridge under ~/mike/uvex
wget --mirror --no-parent --no-verbose -A.sum8,.list --directory-prefix downloaded/ --http-user=$UVEXUSER --http-passwd=$UVEXPASSWD http://apm3.ast.cam.ac.uk/~mike/uvex/
