#!/usr/bin/env python3

from grass.pygrass.modules import Module


def run_knight_path(real_elev, scanned_elev, env, **kwargs):
    # set the computational region
    Module("g.region", raster="elevation")

    charakteristika = """
    1:3:1:1
    4:5:1:1
    6:6:1:1
    7:7:1:1"""

    Module(
        "r.recode",
        input="landclass96",
        output="friction",
        rules="-",
        stdin_=charakteristika,
        overwrite=True,
    )

    Module(
        "r.walk",
        flags="bk",
        elevation=scanned_elev,
        friction="friction",
        output="path",
        outdir="smer",
        start_coordinates=(634935.9292929292, 220446.1085858586),
        overwrite=True,
    )

    Module(
        "r.path",
        input="smer",
        start_coordinates=(637498.2424242424, 218050.57323232322),
        raster_path="path",
        vector_path="path",
        overwrite=True,
    )
