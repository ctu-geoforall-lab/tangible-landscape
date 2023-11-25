#!/usr/bin/env python3

##############################################################################
#
# AUTHOR(S):    Ondrej Pesek
# BASED ON:     github.com/tangible-landscape/tangible-landscape-applications/
##############################################################################

import os
import grass.script as gs
from grass.pygrass.modules import Module
from grass.pygrass.raster.abstract import Info
from grass.exceptions import CalledModuleError

import analyses


os.environ['GRASS_OVERWRITE'] = '1'
os.environ['GRASS_VERBOSE'] = '0'


def run_water(scanned_elev, env, **kwargs):
    Module("g.region", raster=scanned_elev)
    # simwe
    # Module(
    #     "r.slope.aspect",
    #     elevation=scanned_elev,
    #     dx="dx",
    #     dy="dy"
    # )
    # Module(
    #     "r.sim.water",
    #     elevation=scanned_elev,
    #     dx="dx",
    #     dy="dy",
    #     rain_value=300,
    #     depth="depth",
    #     nwalkers=10000,
    #     niterations=5
    # )
    analyses.simwe(
        scanned_elev=scanned_elev, depth="depth", rain_value=300, niterations=5, env=env
    )
    gs.write_command(
        "r.colors",
        map="depth",
        rules="-",
        stdin="0.001 0:128:0\n0.05 0:255:255\n0.1 0:127:255\n0.5 0:0:255\n10 0:0:0",
        env=env,
    )

    # ponds
    try:
        analyses.depression(
            scanned_elev=scanned_elev, new="ponds", repeat=3, filter_depth=0, env=env
        )
    except CalledModuleError:
        return

    # get optimal interval for contours
    info = Info(scanned_elev)
    info.read()
    interval = (info.max - info.min) / 10
    # alternatively set fixed interval
    # interval = 10

    Module(
        "r.contour",
        flags="t",
        input=scanned_elev,
        output="contours",
        step=interval,
    )
