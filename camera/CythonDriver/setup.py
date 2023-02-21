import numpy
from setuptools import setup, Extension
from Cython.Build import cythonize

# Build Environment Variables: CFLAGS="-I/opt/MVS/include"  LDFLAGS="-L/opt/MVS/lib/64"

setup(
    name="mvs_driver",
    version="0.0.1",
    ext_modules=cythonize([
        Extension("mvs_driver", ["mvs_driver.pyx"],
                  libraries=["MvCameraControl",
                             "MvUsb3vTL",
                             "MVGigEVisionSDK",
                             "MediaProcess",
                             "FormatConversion",
                             "MVRender"],
                  include_dirs=[numpy.get_include(), "/opt/MVS/include"]),

    ], language_level="3"),
    requires=["cython"]
)
