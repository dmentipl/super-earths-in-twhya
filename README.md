Super-Earths in the TW Hya disc
===============================

by Daniel Mentiplay, Daniel Price, and Christophe Pinte

* ADS: [2019MNRAS.484L.130M](https://ui.adsabs.harvard.edu/abs/2019MNRAS.484L.130M)
* arXiv: [1811.03636](http://arxiv.org/abs/1811.03636)
* DOI: [10.1093/mnrasl/sly209](https://www.doi.org/10.1093/mnrasl/sly209)

*Note that this repository is not a complete history of the work. We created this repository after the paper was accepted.*

Abstract
--------

We test the hypothesis that the sub-millimetre thermal emission and scattered light gaps seen in recent observations of TW Hya are caused by planet-disc interactions. We perform global three-dimensional dusty smoothed particle hydrodynamics simulations, comparing synthetic observations of our models with dust thermal emission, CO emission and scattered light observations.  We find that the dust gaps observed at 24 au and 41 au can be explained by two super-Earths (approx. 4 Earth-mass). A planet of approximately Saturn-mass can explain the CO emission and the depth and width of the gap seen in scattered light at 94 au. Our model produces a prominent spiral arm while there are only hints of this in the data. To avoid runaway growth and migration of the planets we require a disc mass of less than 0.01 solar masses in agreement with CO observations but 10 to 100 times lower than the estimate from HD line emission.

Results
-------

We aimed to reproduce recent observations of TW Hya.

![Synthetic observations of thermal dust continuum at 870 micron.](alma-image.png)

*Synthetic observations of thermal dust continuum at 870 micron.*

![Synthetic observations of scattered light at 1.6 micron.](scattered-image.png)

*Synthetic observations of scattered light at 1.6 micron.*

Manuscript
----------

The history of the manuscript is a separate private git repository. We include the files here.

Code
----

The code directory contains source code for initialising the models in Phantom, post-processing in MCFOST, and generating figures from the models and observations.

* Phantom `.setup` and `.in` files used to generate the Phantom simulations
* MCFOST `.para` files for thermal dust continuum, scattered light, and CO line
  emission synthetic observations
* Splash config files to produce figures for the paper
* Plus Python scripts to analysis and comparison with observations or
  analytic results

### Reproducibility

We used the Phantom version specified by the following git commit hash: `f0a1825898dc778720d0cccacc4ea403c4c6de40`.

We used the MCFOST version specified by the following git commit hash: `bc332ce`.

Data
----

Data sets are available on Figshare. There are two sets of data:

- [Phantom dust-gas hydrodynamical models](https://figshare.com/articles/dataset/TW_Hya_dust_and_gas_hydrodynamical_models_with_Phantom/11595369)
- [MCFOST radiative transfer post-processed models](https://figshare.com/articles/dataset/TW_Hya_dust_and_gas_radiative_transfer_models_with_MCFOST/11625930)

These data sets contain model snapshots (and post-processed snapshots) used for the publication. For more details on the full data sets see [here](data/README.md).
