#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bulk download USGS GeoPDF maps using The National Map[1] CSV data.

[1]: https://viewer.nationalmap.gov/basic/"""

import argparse
import csv
import os.path
import subprocess
import time

def read(filename):
    """Read TNM CSV data."""

    data = {}
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row["sourceId"]
            name = row["downloadURL"].split("/")[-1]
            data[key] = {"filename": name}
            for k in row:
                data[key][k] = row[k]

    return data

def curl(data, path=None, state=None):
    """Download maps using curl."""

    for k in data:
        filename = data[k]["filename"].replace(".pdf", ".tiff")
        if path and os.path.isfile(os.path.join(path, filename)):
            continue
        elif state and filename[:2] != state:
            continue

        cmd = ["curl", data[k]["downloadURL"], "-o", data[k]["filename"]]
        print(" ".join(cmd))
        subprocess.run(cmd)
        time.sleep(5)  # be nice
        print()

if __name__ == "__main__":
    p = argparse.ArgumentParser(prog="download.py", description=__doc__)
    p.add_argument("-t", "--tiff", dest="path", type=str,
                   help="download only if .tiff does not exists in path")
    p.add_argument("-s", "--state", dest="state", type=str,
                   help="download only for this state")
    p.add_argument(dest="filename", help="TNM .csv filename")

    args = p.parse_args()

    data = read(args.filename)
    curl(data, args.path, args.state)
