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


def run_drainage_path(real_elev, scanned_elev, env, **kwargs):
    Module("g.region", raster=scanned_elev)
    cur_region = Region()
    start_point_coords = (
        cur_region.west + (cur_region.east - cur_region.west) * 2 / 3,
        cur_region.south + (cur_region.north - cur_region.south) * 2 / 3
    )

    Module(
        "r.watershed",
        elevation=scanned_elev,
        drainage="drain_dir",
    )

    Module(
        "r.path",
        input="drain_dir",
        vector_path="drain_path",
        start_coordinates=start_point_coords,
    )
