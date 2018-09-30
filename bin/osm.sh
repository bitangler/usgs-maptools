#!/bin/bash
# Download and process Open Street Maps data.

for tiff in $@; do
    echo $tiff
    basename=`basename $tiff`
    prefix=${basename::-5}

    echo $prefix
    mkdir -p $prefix
    ../bin/osmtrails.py $tiff
    mv ${prefix}* ${prefix}/
done
