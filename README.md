# GMAO compression utilities

## Setup

### Using pixi (recommended)

First, install pixi (if you haven't already) per the default installation instructions here: https://pixi.sh/latest/installation/.
Note that this is a user-level install (i.e., installs to your home directory); you don't need any kind of admin privileges.
You only need to do this once per system.
Then, log out and log back in (or `source ~/.bashrc`).

Once pixi is installed, you can "activate" this environment with:

```sh
pixi shell
```

...or run specific scripts with `pixi run`:

```sh
pixi run python scripts/calc_keepbits.py
```

This will first install all project dependencies before running the actual scripts.

### Using mamba (only on NCCS Discover)

Load python environment.

```sh
module purge
module load python/GEOSpyD/24.11.3-0/3.13
```

Confirm that `mamba` executable is present.

```sh
which mamba
```

If you haven't done something similar already,
configure `mamba` to cache to your `$NOBACKUP` directory.
Otherwise, it will quick fill up your home directory quota.

```sh
mkdir -p $NOBACKUP/.mamba
ln -s $NOBACKUP/.mamba $HOME/.mamba
```

Create environment and install dependencies.
(NOTE: Replace `./compression-env` with any relative or absolute path corresponding to the location where you want to store the environment.)

```sh
mamba create -p ./compression-env xarray xbitinfo zstandard netcdf4 conda
```

Activate the environment:

```sh
eval "$(mamba shell hook --shell bash)"
mamba activate ./compression-env
export CONDA_JL_CONDA_EXE=$(which conda)
```

## Usage

(If using mamba, first activate the environment as above; then run these scripts without the `pixi run` prefix).

```sh
# Download test data
bash scripts/get-test-data.sh

# Calculate keepbits on test data
pixi run python scripts/calc_keepbits.py

# Compress the files
pixi run python scripts/compress.py

# Compare the file sizes
pixi run python scripts/compare-sizes.py
```
