# -*- coding: utf-8 -*-

from __future__ import division, print_function

import numpy as np
from astropy.io import fits

__all__ = ["get_light_curve"]

def _everest_url_and_fn(campaign, epicid):
    id_str = "{0:09d}".format(epicid)
    fn = "hlsp_everest_k2_llc_{0}-c{1:02d}_kepler_v2.0_lc.fits".format(
        id_str, campaign
    )
    url = "https://archive.stsci.edu/missions/hlsp/everest/v2/"
    url += "c{0:02d}/{1}00000/{2}/".format(campaign, id_str[:4], id_str[4:])
    return url + fn, fn

def get_light_curve(campaign, epicid):
    url, fn = _everest_url_and_fn(campaign, epicid)
    with fits.open(url, cache=False) as hdus:
        data = hdus[1].data
        t = data["TIME"]
        q = data["QUALITY"]
        f = data["FLUX"]
    m = np.isfinite(t) & np.isfinite(f) & (q == 0)
    f = f[m]
    f = (f / np.median(f) - 1.0) * 100.0
    return (
        np.ascontiguousarray(t[m], dtype=np.float64),
        np.ascontiguousarray(f, dtype=np.float64)
    )
