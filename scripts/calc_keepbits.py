#!/usr/bin/env python

from pathlib import Path

import xbitinfo
import xarray as xr
import pandas as pd

files = [
    "_data/GiOCEAN_e1.atm_inst_6hr_glo_L720x361_p49.20241101_0600z.nc4",
    "_data/GiOCEAN_e1.atm_inst_6hr_glo_L720x361_p49.20241101_1800z.nc4",
    "_data/GiOCEAN_e1.sfc_tavg_3hr_glo_L720x361_sfc.20241101_0730z.nc4",
    "_data/GiOCEAN_e1.sfc_tavg_3hr_glo_L720x361_sfc.20241101_1930z.nc4"
]

def calc_keepbits(fname):
    ds = xr.open_dataset(fname)
    kbdims = [dim for dim, size in ds.sizes.items() if size > 6]
    bitinfo = xbitinfo.get_bitinformation(ds, dim=kbdims)

    keepbits = xbitinfo.get_keepbits(bitinfo, inflevel=[0.999, 0.995, 0.99, 0.95])
    kbmax = keepbits.max(dim='dim')

    kbdat = kbmax.to_pandas().transpose()
    outdir = Path("_keepbits")
    outdir.mkdir(exist_ok = True)
    outfile = outdir / (Path(fname).stem + ".csv")
    kbdat.to_csv(outfile)

[calc_keepbits(fname) for fname in files]
