#!/usr/bin/env python3
"""Determine the cutline polygon for a USGS GeoPDF."""

import argparse
import json
from osgeo import gdal, osr
import sys

def polygon(neatline):
    """Polygon coordinates from USGS NEATLINE metadata."""

    neatline = neatline.replace("POLYGON ((", "").replace("))", "")

    p = []
    for xy in neatline.split(","):
        x, y = [float(i) for i in xy.split(" ")]
        p.append([x, y])

    return [p]

def crs_name(geopdf):
    """GeoJSON CRS name attribute from GeoPDF."""

    prj = geopdf.GetProjection()

    srs = osr.SpatialReference(wkt=prj)
    epsg = srs.GetAttrValue("AUTHORITY", 1)
    return "urn:ogc:def:crs:EPSG::{}".format(epsg)

def geojson(filename):
    """Cutline as GeoJSON."""

    usgs = gdal.Open(filename)
    meta = usgs.GetMetadata()

    coordinates = polygon(meta["NEATLINE"])
    name = crs_name(usgs)
    cutline = {"type": "FeatureCollection",
               "crs": {"type": "name", "properties": {"name": name}},
               "features": [{"type": "Feature",
                             "properties": {"id": None},
                             "geometry": {"type": "Polygon",
                                          "coordinates": coordinates}}]}

    print(json.dumps(cutline))

if __name__ == "__main__":
    p = argparse.ArgumentParser(prog="cutline.py", description=__doc__)
    p.add_argument("-o", dest="outfile", help="Output filename")
    p.add_argument(dest="filename", help="USGS GeoPDF filename")

    args = p.parse_args()

    if args.outfile:
        sys.stdout = open(args.outfile, "w")

    geojson(args.filename)
