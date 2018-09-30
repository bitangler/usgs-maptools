#!/usr/bin/env python3
"""Determine the bounding box of a USGS GeoPDF."""

from osgeo import gdal, osr
import urllib.parse
import utm

def bbox(filename):
    """Bounding box for USGS GeoPDF as WGS84 list."""

    usgs = gdal.Open(filename)
    meta = usgs.GetMetadata()
    zone = utm_zone(usgs)

    neatline = meta["NEATLINE"].replace("POLYGON ((", "").replace("))", "")

    LAT = []
    LON = []
    for xy in neatline.split(","):
        x, y = [float(i) for i in xy.split(" ")]
        lat, lon = utm.to_latlon(x, y, zone, "N")
        LAT.append(lat)
        LON.append(lon)

    return [min(LON), min(LAT), max(LON), max(LAT)]

def utm_zone(usgs):
    """UTM Zone"""

    prj = usgs.GetProjection()
    srs = osr.SpatialReference(wkt=prj)
    return srs.GetUTMZone()
