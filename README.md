# whitening-filter

`whitening-filter` is a Python tool for whitening pink noise or 1/f noise, with a 1/f^{\beta} power spectral density. The code is based upon the wavelet transform and uses algorithms in *Numerical Recipes in C* (Press et al. 1992) and [Carter & Winn (2009)](https://ui.adsabs.harvard.edu/abs/2009ApJ...704...51C/abstract). 

**Author**: Gavin Wang

## Usage
1. Clone the repository, as in `git clone https://github.com/gavinxwang/whitening-filter.git`
2. Compile the `dwt.c` code
3. Create some colored noise to input `solveredwv.py` 

<!-- ## Installation -->

## Acknowledgments

If you use this code, please cite *Numerical Recipes in C* (Press et al. 1992) and [Carter & Winn (2009)](https://ui.adsabs.harvard.edu/abs/2009ApJ...704...51C/abstract) and provide a link to this repository.
