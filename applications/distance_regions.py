#!/usr/bin/env python3

############################################################################
#
# AUTHOR(S):    Lucie Antosova, Katerina Boudova, Barbora Dvorakova,
#               Martina Kulikova
#               Ondrej Pesek
############################################################################

import os

from grass.pygrass.modules import Module
from grass.pygrass.gis.region import Region

os.environ['GRASS_OVERWRITE'] = '1'
os.environ['GRASS_VERBOSE'] = '0'


def run_distance_regions(real_elev, scanned_elev, env, **kwargs):
    Module("g.region", raster=scanned_elev)
    cur_region = Region()
    start_point_coords = (
        cur_region.west + (cur_region.east - cur_region.west) * 2 / 3,
        (cur_region.north + cur_region.south) / 2
    )

    characteristics = """
    1:3:1:1
    4:5:1:1
    6:6:1:1
    7:7:1:1
    """

    Module(
        "r.recode",
        input="landclass96",
        output="friction",
        rules="-",
        stdin_=characteristics,
    )

    Module(
        "v.in.ascii",
        input="-",
        output="start_point",
        stdin_=f"{start_point_coords[0]}|{start_point_coords[1]}",
    )

    Module(
        "r.walk",
        flags="k",
        elevation=scanned_elev,
        friction="friction",
        output="walkcost",
        start_coordinates=start_point_coords,
        max_cost=10000,
        lambda_=0.5
    )

    Module(
        "r.contour",
        input="walkcost",
        output="walkcost_borders",
        step=1000,
    )
