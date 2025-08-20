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
    kbfile = Path("_keepbits/") / (Path(fname).stem + ".csv")
    outdir = Path("_compressed")
    outdir.mkdir(exist_ok=True)
    outfile = outdir / Path(fname).name
    kb = pd.read_csv(kbfile, index_col=0)
    kb_selected = kb.loc[:, "0.99"]
    # Note: Remove variables with negative or zero keepbits (this is likely a bug)
    kb_selected = kb_selected[kb_selected > 0]
    input = xr.open_dataset(fname, engine="netcdf4")
    enc = {
        key: {
            "compression": "zlib",
            "shuffle": True,
            "significant_digits": value,
            "quantize_mode": "BitRound",
        }
        for key, value in kb_selected.items()
    }
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
