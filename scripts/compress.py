#!/usr/bin/env python

from pathlib import Path

import subprocess
import pandas as pd

import xarray as xr
import humanize

files = [
    "_data/GiOCEAN_e1.atm_inst_6hr_glo_L720x361_p49.20241101_0600z.nc4",
    "_data/GiOCEAN_e1.atm_inst_6hr_glo_L720x361_p49.20241101_1800z.nc4",
    "_data/GiOCEAN_e1.sfc_tavg_3hr_glo_L720x361_sfc.20241101_0730z.nc4",
    "_data/GiOCEAN_e1.sfc_tavg_3hr_glo_L720x361_sfc.20241101_1930z.nc4",
]

fname = files[2]


def compress(fname):
    outdir = Path("_compressed")
    outdir.mkdir(exist_ok=True)
    outfile = outdir / Path(fname).name
    # NOTE: In production, we will not have separate keepbits for every file. 
    # We need to read a representative sample of the keepbits data, get a 
    # conservative estimate of the keepbits (maximum value for each variable), 
    # and then apply that uniformly to the files to be compressed.
    kbfile = Path("_keepbits/") / (Path(fname).stem + ".csv")
    kb = pd.read_csv(kbfile, index_col=0)
    kb_selected = kb.loc[:, "0.99"]
    # Keepbits <= 0 are a bug, so just remove those variables; we'll preserve 
    # their native encoding.
    kb_selected = kb_selected[kb_selected > 0]
    input = xr.open_dataset(fname, engine="netcdf4")
    # Enable compression for *all* variables
    enc = {
        key: {
            "compression": "zlib",
            "shuffle": True
        }
        for key in input.data_vars.keys()
    }
    # ...and then *also* do bitround on the ones with keepbits
    for key, value in kb_selected.items():
        enc[key] |= {"significant_digits": value, "quantize_mode": "BitRound"}
    input.to_netcdf(
        outfile,
        engine="netcdf4",
        encoding=enc
    )
    orig_size = Path(fname).stat().st_size
    new_size = Path(outfile).stat().st_size
    ratio = orig_size / new_size
    print(f"File: {fname} --> {outfile}")
    print(f"Original: {humanize.naturalsize(orig_size)}")
    print(f"Compressed: {humanize.naturalsize(new_size)}")
    print(f"Ratio: {ratio:.2f}")

for fname in files:
    compress(fname)
