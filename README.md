# whitening-filter

`whitening-filter` is a Python tool for whitening pink noise or 'flicker noise,' which has a 1/f power spectral density. This code is based upon the wavelet transform and uses algorithms in *Numerical Recipes in C* (Press et al. 1992) and [Carter & Winn (2009)](https://ui.adsabs.harvard.edu/abs/2009ApJ...704...51C/abstract). 

**Author**: Gavin Wang ([gxwang22@gmail.com](gxwang22@gmail.com))

## Overview

This library uses likelihood maximization to estimate the red and white noise components of a 1-D time series. 

## Installation and Usage

1. Clone the repository (e.g., `git clone https://github.com/gavinxwang/whitening-filter.git`).
2. Run `python setup.py install` to interface the `dwt.c` code with Python. This only needs to be done the first time you use this script. If you want to re-install, you will need to delete the corresponding folder in `site-packages`.
3. Verify that the setup has been successful by typing `import dwt` in Python.
4. As a simple test, you can perform the forward wavelet transform of a vector (`dwt.call_wt1(x,1)`) and subsequently the inverse transform (`dwt.call_wt1(c,-1)`) on the coefficients -- you should get back the same input vector.
5. To whiten colored noise, the function to call is `solveredwv` -- an example pink noise sequence is stored in `vector.txt`.

## Notes

If the filter does not seem to accurately predict the white and red noise components of a time series, try increasing the length of the time series. Additionally, the current code has $\gamma$ fixed at 1 (where $\gamma$ describes the color of the noise, with power 1/f^$\gamma$), but it can be adapted to cases where $\gamma$ deviates (slightly but not too much) from 1. 

These scripts have been cross-checked with and agree with the IDL implementation of the same routine found [here](https://github.com/zgazak/TAP/tree/master/extra_pro/carter_winn_wavelets).

## Acknowledgments

If you use this code, please cite [Carter & Winn (2009)](https://ui.adsabs.harvard.edu/abs/2009ApJ...704...51C/abstract) and provide a link to this repository.

Feel free to reach out with any questions.
