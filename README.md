# GMAO compression utilities

## Setup on NCCS Discover

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

Install the library itself.

```sh
# Confirm that you are using pip from the compression environment 
which pip
# Now, install
pip install .
```

Confirm the installation:

```sh
compress --help
```

## Usage

Activate the environment.

```sh
eval "$(mamba shell hook --shell bash)"
mamba activate ./compression-env
export CONDA_JL_CONDA_EXE="$(which conda)"
```

Then use one of the following commands as appropriate:

```sh
compress --help
decompress --help
verify --help
```
