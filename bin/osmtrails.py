#!/usr/bin/env python3
"""Extract Open Street Map trails for a USGS GeoPDF."""

import argparse
import boundbox
from bs4 import BeautifulSoup
import os
import re
import urllib.request

# OSM highway tags that may be trails
# see: https://wiki.openstreetmap.org/wiki/Key:highway
TAGS = ["bridleway", "cycleway", "footway", "path", "pedestrian", "track"]

def catalog(filename, trails):
    """Catalog trails in OSM dataset."""

    soup = download(filename)

    for way in soup.find_all("way"):
        for tag in way.find_all("tag"):
            if tag["k"] == "highway" and tag["v"] in TAGS:
                data = meta(way)
                if data["name"]:
                    for k in trails:
                        if re.search(k, data["name"], re.I):
                            trails[k].append(data)
                            break
                    else:
                        trails["trails"].append(data)
                else:
                    trails["trails"].append(data)

def download(filename):
    """Download OSM data within USGS GeoPDF bounding box."""

    url = "https://api.openstreetmap.org/api/0.6/map?bbox={0},{1},{2},{3}"
    bbox = boundbox.bbox(filename)

    with urllib.request.urlopen(url.format(*bbox)) as osm:
        soup = BeautifulSoup(osm.read(), "lxml-xml")

    return soup

def meta(way):
    """Waypoint metadata."""

    data = {"id": way["id"], "name": None, "nodes": nodes(way)}
    for tag in way.find_all("tag"):
        data[tag["k"]] = tag["v"]
    return data

def nodes(way):
    """Waypoint reference nodes."""

    data = []
    for nd in way.find_all("nd"):
        data.append(nd["ref"])
    return data

def strip(filename, trails, outfile):
    """Strip everything but trail data from OSM dataset."""

    soup = download(filename)

    for node in soup.find_all("node"):
        for trail in trails:
            if node["id"] in trail["nodes"]:
                break
        else:
            node.decompose()

    for way in soup.find_all("way"):
        for trail in trails:
            if way["id"] == trail["id"]:
                break
        else:
            way.decompose()

    for relation in soup.find_all("relation"):
        relation.decompose()

    with open(outfile, "w") as out:
        out.write(soup.prettify())

if __name__ == "__main__":
    p = argparse.ArgumentParser(prog="osmtrails.py", description=__doc__)
    p.add_argument(dest="filename", help="USGS GeoPDF")

    args = p.parse_args()

    prefix, ext = os.path.splitext(os.path.basename(args.filename))

    # trails to catalog
    trails = {"appalachian": [],
              "massanutten": [],
              "tuscarora": [],
              "trails": []  # everything else
    }

    catalog(args.filename, trails)

    for k in trails:
        if len(trails[k]) == 0:
            continue

        outfile = "{}_{}.osm".format(prefix, k)
        print(outfile, len(trails[k]))
        strip(args.filename, trails[k], outfile)
