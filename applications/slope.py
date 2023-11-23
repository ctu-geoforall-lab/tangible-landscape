#!/usr/bin/env python3

##############################################################################
#
# AUTHOR(S):    Ondrej Pesek
# BASED ON:     github.com/tangible-landscape/tangible-landscape-applications/
##############################################################################

import os

from grass.pygrass.modules import Module

os.environ['GRASS_OVERWRITE'] = '1'
os.environ['GRASS_VERBOSE'] = '0'


def run_slope(real_elev, scanned_elev, env, **kwargs):
    Module("g.region", raster=scanned_elev)

    Module("r.slope.aspect", elevation=scanned_elev, slope="slope")

    # get optimal interval for contours
    info = Info(scanned_elev)
    info.read()
    interval = (info.max - info.min) / 20
    # alternatively set fixed interval
    # interval = 10

    Module(
        "r.contour",
        flags="t",
        input=scanned_elev,
        output="contours",
        step=interval,
    )
