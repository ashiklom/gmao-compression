#!/usr/bin/env python

from pathlib import Path
import humanize

files = [
    "_data/GiOCEAN_e1.atm_inst_6hr_glo_L720x361_p49.20241101_0600z.nc4",
    "_data/GiOCEAN_e1.atm_inst_6hr_glo_L720x361_p49.20241101_1800z.nc4",
    "_data/GiOCEAN_e1.sfc_tavg_3hr_glo_L720x361_sfc.20241101_0730z.nc4",
    "_data/GiOCEAN_e1.sfc_tavg_3hr_glo_L720x361_sfc.20241101_1930z.nc4",
]

for fname in files:
    outdir = Path("_compressed")
    outfile = outdir / Path(fname).name
    orig_size = Path(fname).stat().st_size
    new_size = Path(outfile).stat().st_size
    ratio = orig_size / new_size
    print(f"File: {fname} --> {outfile}")
    print(f"Original: {humanize.naturalsize(orig_size)}")
    print(f"Compressed: {humanize.naturalsize(new_size)}")
    print(f"Ratio: {ratio:.2f}")
    print("-"*10)
