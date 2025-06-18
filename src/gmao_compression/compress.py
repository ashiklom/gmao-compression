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

    # Find all dims with length at least 5
    kb_dims = [dim for dim, size in ds.sizes.items() if size >= 5]

    bitinfo = xb.get_bitinformation(ds, dim=kb_dims)
    keepbits = xb.get_keepbits(bitinfo, inflevel=inflevel)
    kbmax = keepbits.max(dim="dim")

    # Skip variables with negative keepbits
    neg_data = {}
    for v, kb in kbmax.items():
        if kb.item() < 0:
            neg_data[v] = ds[v]
            ds_round = ds_round.drop_vars(v)
            kbmax = kbmax.drop_vars(v)

    if neg_data:
        print(f"Skipping variables with negative keepbits: {set(neg_data.keys())}")
        print(f"Keeping these variables: {set(kbmax.keys())}")

    ds_bitrounded = xb.xr_bitround(ds_round, kbmax)

    # Add skipped variables back in
    for v, arr in {**coord_data, **neg_data}.items():
        ds_bitrounded[v] = arr

    # Apply encodings
    for v in ds_bitrounded.keys():
        ds_bitrounded[v].encoding = {"zlib": True, "complevel": deflate_level}

    print(f"Writing result to {output_file}")
    ds_bitrounded.to_netcdf(
        path=output_file, mode="w", format="NETCDF4", engine="netcdf4"
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
