#!/usr/bin/env python3
"""Determine magnetic declination from USGS GeoPDF."""

# Uses the NOAA Magnetic Declination Calculator[1].
# [1]: https://www.ngdc.noaa.gov/geomag-web/calculators/declinationHelp

import argparse
import boundbox
from bs4 import BeautifulSoup
from datetime import datetime
from osgeo import gdal, osr
import urllib.parse
import urllib.request

NOAA = "https://www.ngdc.noaa.gov/geomag-web/calculators/calculateDeclination?{}"

def declination(bbox, date):
    """NOAA magnetic declination from WGS84 bounding box."""

    # center of bounding box
    lon = 0.5*(bbox[0] + bbox[2])
    lat = 0.5*(bbox[1] + bbox[3])

    params = urllib.parse.urlencode({"lat1": lat, "lon1": lon,
                                     "startYear": date.year,
                                     "startMonth": date.month,
                                     "startDay": date.day,
                                     "resultFormat": "xml"})

    with urllib.request.urlopen(NOAA.format(params)) as noaa:
        soup = BeautifulSoup(noaa, "lxml-xml")

    #print(soup.prettify())
    return float(soup.result.declination.text)

if __name__ == "__main__":
    p = argparse.ArgumentParser(prog="magdecl.py", description=__doc__)
    p.add_argument(dest="filename", help="USGS GeoPDF")

    args = p.parse_args()

    now = datetime.now()
    bbox = boundbox.bbox(args.filename)
    d = declination(bbox, now)

    date = now.strftime("%Y-%m-%d")
    print("Magnetic Declination = {:.1f}° ({})".format(d, date))
