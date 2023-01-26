#!/usr/bin/env python3

############################################################################
#
# AUTHOR(S):    Lucie Antosova, Katerina Boudova, Barbora Dvorakova,
#               Martina Kulikova
#               Ondrej Pesek
############################################################################

from grass.pygrass.modules import Module


def run_drainage_path(real_elev, scanned_elev, env, **kwargs):
    Module("g.region", flags="p", raster=scanned_elev)

    Module(
        "r.watershed",
        elevation=scanned_elev,
        accumulation="accum",
        drainage="drain_dir",
        overwrite=True,
    )

    Module(
        "r.mapcalc",
        expression="drain_deg = if(drain_dir != 0, 45. * abs(drain_dir), null())",
        overwrite=True,
    )

    Module(
        "r.path",
        input="drain_deg",
        raster_path="drain_path",
        vector_path="drain_path",
        start_coordinates=(635184, 226127),
        overwrite=True,
    )

    Module("r.colors", map=scanned_elev, color="elevation", overwrite=True)

    Module("r.relief", input=scanned_elev, output="relief", overwrite=True)
