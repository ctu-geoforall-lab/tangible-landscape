#!/usr/bin/env python3

##############################################################################
#
# AUTHOR(S):    Ondrej Pesek
# BASED ON:     github.com/tangible-landscape/tangible-landscape-applications/
##############################################################################

import os

from grass.pygrass.modules import Module
from grass.pygrass.raster.abstract import Info

os.environ['GRASS_OVERWRITE'] = '1'
os.environ['GRASS_VERBOSE'] = '0'


def run_contours(real_elev, scanned_elev, env, **kwargs):
    Module("g.region", raster=scanned_elev)

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
        output="contours_main",
        step=interval * 5,
    )

    Module(
        "r.contour",
        flags="t",
        input=scanned_elev,
        output="contours",
        step=interval,
    )
