# whitening-filter

`whitening-filter` is a Python tool for whitening pink noise or 'flicker noise,' which has a 1/f power spectral density. This code is based upon the wavelet transform and uses algorithms in *Numerical Recipes in C* (Press et al. 1992) and [Carter & Winn (2009)](https://ui.adsabs.harvard.edu/abs/2009ApJ...704...51C/abstract). 

**Author**: Gavin Wang ([gxwang22@gmail.com](gxwang22@gmail.com))

## Installation and Usage

Simply clone the repository (e.g., `git clone https://github.com/gavinxwang/whitening-filter.git`), compile the `dwt.c` code, create some colored noise and you are good to go! The script to run is `solveredwv.py` -- an example noise sequence is stored in `x` under the `main` function.

## Notes

If the filter does not seem to be accurately predicting the white and red noise components of a time series, try increasing the length of the data. Additionally, the current code has $\gamma$ fixed at 1 (where $\gamma$ describes the color of the noise), but it can be easily adapted to cases where $\gamma$ deviates significantly from 1.

## Acknowledgments

If you use this code, please cite *Numerical Recipes in C* (Press et al. 1992) and [Carter & Winn (2009)](https://ui.adsabs.harvard.edu/abs/2009ApJ...704...51C/abstract), and provide a link to this repository.

Feel free to reach out with any quesitons.
