"""Format UTM grid points."""

from qgis.core import *
from qgis.gui import *
from math import floor

superscript = [u"\u2070", u"\u00B9", u"\u00B2", u"\u00B3", u"\u2074",
               u"\u2075", u"\u2076", u"\u2077", u"\u2078", u"\u2079"]

@qgsfunction(args="auto", group="Custom")
def utmlabel(grid_number, feature, parent):
    """Converts grid_number to a formatted UTM label."""

    i = int(grid_number)
    n = int(floor(i / 100000.0))
    m = int(floor((i - 100000*n) / 1000.0))

    out = ""
    for k in "%d" % n:
        out += superscript[int(k)]
    out += "%02d" % m

    return out
