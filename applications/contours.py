#!/usr/bin/env python3

##############################################################################
#
# AUTHOR(S):    Ondrej Pesek
# BASED ON:     github.com/tangible-landscape/tangible-landscape-applications/
##############################################################################

from grass.pygrass.modules import Module
from grass.pygrass.raster.abstract import Info


def run_contours(real_elev, scanned_elev, env, **kwargs):
    Module("g.region", raster=scanned_elev)

    # get optimal interval
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
        quiet=True,
        overwrite=True,
    )

    Module(
        "r.contour",
        flags="t",
        input=scanned_elev,
        output="contours",
        step=interval,
        quiet=True,
        overwrite=True,
    )
