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


def run_knight_path(real_elev, scanned_elev, env, **kwargs):
    Module("g.region", raster=scanned_elev)
    cur_region = Region()
    start_point_coords = (
        cur_region.west + (cur_region.east - cur_region.west) * 3 / 4,
        cur_region.south + (cur_region.north - cur_region.south) * 3 / 4
    )
    end_point_coords = (
        cur_region.west + (cur_region.east - cur_region.west) * 1 / 4,
        cur_region.south + (cur_region.north - cur_region.south) * 1 / 4
    )

    characteristics = """
    1:3:1:1
    4:5:1:1
    6:6:1:1
    7:7:1:1"""

    Module(
        "r.recode",
        input="landclass96",
        output="friction",
        rules="-",
        stdin_=characteristics,
    )

    Module(
        "r.walk",
        flags="bk",
        elevation=scanned_elev,
        friction="friction",
        output="costs",
        outdir="smer",
        start_coordinates=start_point_coords,
        walk_coeff=(0.72,12.0,1.9998,-1.9998)
    )

    Module(
        "r.path",
        input="smer",
        start_coordinates=end_point_coords,
        vector_path="path",
    )
