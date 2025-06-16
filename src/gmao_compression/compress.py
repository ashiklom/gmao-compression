#!/usr/bin/env python

import argparse

import xarray as xr
import xbitinfo as xb


def xbitinfo_round(input_file, inflevel, output_file, deflate_level=2):
    ds = xr.open_dataset(input_file)
    coord_vars = list(ds.coords)

    if "TAITIME" in list(ds.data_vars):
        coord_vars.append("TAITIME")
    coord_data = {var: ds[var] for var in coord_vars if var in ds}
    ds_round = ds.drop_vars(coord_vars)

    bitinfo = xb.get_bitinformation(ds, dim="lon")
    keepbits = xb.get_keepbits(bitinfo, inflevel=inflevel)

    neg_vars = [v for v, kb in keepbits.items() if kb.item() < 0]
    if neg_vars:
        print(f"Skipping variables with negative keepbits: {neg_vars}")
        neg_data = {v: ds[v] for v in neg_vars}
        ds_round = ds_round.drop_vars(neg_vars)
        # remove them from the keepbits dict so xr_bitround won’t see them
        keepbits = {v: kb for v, kb in keepbits.items() if v not in neg_vars}
    else:
        neg_data = {}

    keepbits = {var: int(kb.item()) for var, kb in keepbits.items()}

    ds_bitrounded = xb.xr_bitround(ds_round, keepbits)

    for v, arr in {**coord_data, **neg_data}.items():
        ds_bitrounded[v] = arr

    ds_bitrounded.to_netcdf(
        path=output_file,
        mode="w",
        format="NETCDF4",
        engine="netcdf4",
        encoding={"zlib": True, "compression": deflate_level},
    )

    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Apply xbitinfo rounding in memory and compress the result with zstd."
    )
    parser.add_argument("file_path", help="Path to the input NetCDF file")
    parser.add_argument(
        "compression_level", type=float, help="Rounding level for xbitinfo rounding"
    )
    parser.add_argument("output_path", help="Path to write the compressed file")
    parser.add_argument("deflate_level", help="DEFLATE compression level", default=2)
    args = parser.parse_args()

    xbitinfo_round(
        args.file_path,
        args.compression_level,
        args.output_path,
        deflate_level=args.deflate_level,
    )

    print(f"Compressed file written to: {args.output_path}")


if __name__ == "__main__":
    main()
