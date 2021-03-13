Super Earths in the TW Hya disc data
====================================

*Note: The full data sets are not publicly available but will be upon request. See Figshare for publicly available reduced data sets. (URLs are in the top-level [README.md](../README.md) file.)*

This file contains instructions on acquiring data for the TW Hya models. There are Phantom-related data and MCFOST-related data. There are two sets of models.

* One focussing on the inner planets with dust and gas modelling: `dust-gas`. For each planet mass of 4, 8, and 16 Earth masses, we ran two single-grain-size calculations at 100 micron and 1 mm.
* The other focussing on the outer planet with gas-only models: `gas-only`. We ran four models with planet masses 0.1, 0.3, 1, and 2 Jupiter masses.

The following uses the shell variable `ROOT_DIR` which specifies the location of the data on the file system.

Raw Phantom data
----------------

The Phantom dumps are in the two sub-directories `dust-gas` and `gas-only`. The sub-directory (of `dust-gas` and `gas-only`) containing the raw Phantom data is `00_raw_phantom_data`. There is a directory for each planet mass, and in the dust and gas models there is a directory for each grain size for each planet mass.

To get the raw Phantom data:

```bash
scp $ROOT_DIR/dust-gas/00_raw_phantom_data dust+gas_raw_data
scp $ROOT_DIR/gas-only/00_raw_phantom_data gas-only_raw_data
```

Dust-stacked data
-----------------

The dust and gas models have simulations per grain size. They are stacked together to form a single Phantom dump with both grain sizes. There is only one per planet mass for the dump number 250. The data is in `10_stacked_phantom_data` for the `dust-gas` models.

To get the dust-stacked data:

```bash
scp $ROOT_DIR/dust-gas/10_stacked_phantom_data dust+gas_stacked_data
```

MCFOST data
-----------

The FITS files and MCFOST parameter files of the post-processed TW Hya models are in `dust-gas/20_mcfost_post_processed_data` and `gas-only/10_mcfost_post_processed_data`. For the dust and gas models with different inner planet masses there are images of dust thermal emission. For the gas-only models with different outer planet masses we produced scattered light images at 1.6 micron, and CO emission with the full channel maps.

Each directory contains the FITS file with the image data, and the MCFOST parameter file used to generate the image. The git SHA of the MCFOST version used is `639e55cdcfa9c369859001be12e0ab48f68ebf70`.

To get the MCFOST post-processed data:

```bash
scp $ROOT_DIR/dust-gas/20_mcfost_post_processed_data dust+gas_mcfost_data
scp $ROOT_DIR/gas-only/20_mcfost_post_processed_data gas-only_mcfost_data
```

CASA data
---------

The FITS files of the CASA ALMA post-processed dust thermal emission are in `dust-gas/30_casa_post_processed_data`.

To get the CASA post-processed data:

```bash
scp $ROOT_DIR/dust-gas/30_casa_post_processed_data dust+gas_casa_data
```
