#!/usr/bin/env python3

from grass.pygrass.modules import Module


def run_distances(real_elev, scanned_elev, env, **kwargs):


    Module('g.region', raster=scanned_elev)


    charakteristika = """


    1:3:1:1


    4:5:1:1


    6:6:1:1


    7:7:1:1


    """


    Module('r.recode', input='landclass96', output='friction',


           rules='-', stdin_=charakteristika, overwrite=True)


    kwargs={'lambda':0.5}


    Module('r.walk', flags='k', elevation=scanned_elev,


           friction='friction', output='walkcost', outdir='direction',


           start_coordinates=[636235.2631578947,218558.48225214198], max_cost = 10000, overwrite=True, **kwargs)


    Module('r.contour', input = 'walkcost', output = 'walkcost', step = 100, overwrite=True)






