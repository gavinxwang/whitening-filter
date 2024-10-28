import numpy
from setuptools import setup, Extension

# Define the extension module
dwt_module = Extension(
    "dwt",
    sources=["dwt.c", "nrutil.c"],
    include_dirs=[numpy.get_include()]
)

# Setup script
setup(
    name="dwt",
    version="1.0",
    description="whitening-filter module",
    url="https://github.com/gavinxwang/whitening-filter/",
    author="Gavin Wang",
    author_email="gxwang22@gmail.com",
    license="MIT",
    install_requires=['numpy', 'scipy'],
    ext_modules=[dwt_module]
)
