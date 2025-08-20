#!/usr/bin/env python

from pathlib import Path
import humanize

import xarray as xr
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

files = [
    "_data/GiOCEAN_e1.atm_inst_6hr_glo_L720x361_p49.20241101_0600z.nc4",
    "_data/GiOCEAN_e1.atm_inst_6hr_glo_L720x361_p49.20241101_1800z.nc4",
    "_data/GiOCEAN_e1.sfc_tavg_3hr_glo_L720x361_sfc.20241101_0730z.nc4",
    "_data/GiOCEAN_e1.sfc_tavg_3hr_glo_L720x361_sfc.20241101_1930z.nc4",
]

def visual_comparison(fname):
    outdir = Path("_compressed")
    outfile = outdir / Path(fname).name
    pdfdir = Path("_figures")
    pdfdir.mkdir(exist_ok=True)
    pdffile_dir = pdfdir / (Path(fname).stem)
    pdffile_dir.mkdir(exist_ok=True)
    orig = xr.open_dataset(fname)
    comp = xr.open_dataset(outfile)
    diff = comp - orig
    for var_name, var_data in diff.data_vars.items():
        dat = var_data
        if 'lev' in var_data.dims:
            dat = dat.isel(lev=0)
        if 'time' in dat.dims:
            dat = dat.isel(time=0)
        fig = plt.figure(figsize=(6, 3))
        ax = plt.axes()
        dat.plot(ax=ax, cmap="RdBu")
        plt.title(f"{var_name}")
        plt.savefig(pdffile_dir / f'{var_name}.png')
        plt.close()

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
    print("Drawing visual comparison...")
    visual_comparison(fname)
    print("-"*10)
