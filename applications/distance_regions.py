#!/usr/bin/env python3

############################################################################
#
# AUTHOR(S):    Lucie Antosova, Katerina Boudova, Barbora Dvorakova,
#               Martina Kulikova
#               Ondrej Pesek
############################################################################

from grass.pygrass.modules import Module
from grass.pygrass.gis.region import Region


def run_distance_regions(real_elev, scanned_elev, env, **kwargs):
    cur_region = Region()
    center_coords = (
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
        overwrite=True,
        quiet=True
    )

    Module(
        "v.in.ascii",
        input="-",
        output="start_point",
        stdin_=f"{center_coords[0]}|{center_coords[1]}",
        quiet=True,
        overwrite=True,
    )

    Module(
        "r.walk",
        flags="k",
        elevation=scanned_elev,
        friction="friction",
        output="walkcost",
        # outdir="direction",
        start_coordinates=center_coords,
        max_cost=10000,
        overwrite=True,
        quiet=True,
        lambda_=0.5
    )

    Module(
        "r.contour",
        input="walkcost",
        output="walkcost_borders",
        step=1000,
        quiet=True,
        overwrite=True
    )
