#!/usr/bin/env python3

import grass.script as gs


def run_watershed(real_elev, scanned_elev, env, **kwargs):

    gs.run_command('g.region', flags='p',  raster=scanned_elev)


    gs.run_command('r.watershed', elevation=scanned_elev, 

                    accumulation='accum', drainage='drain_dir', overwrite=True)

    gs.run_command('r.mapcalc', 

                    expression="drain_deg = if(drain_dir != 0, 45. * abs(drain_dir), null())", 

                    overwrite=True)

    gs.run_command('r.path', input='drain_deg', raster_path='drain_path',

                    vector_path='drain_path', start_coordinates=(635184 ,226127 ), overwrite=True)

    gs.run_command('r.colors', map=scanned_elev, color='elevation', overwrite=True)

    gs.run_command('r.relief', input=scanned_elev, output='relief', overwrite=True)

