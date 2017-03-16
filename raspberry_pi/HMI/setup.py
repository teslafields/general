from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

import os
ext_modules=[
    Extension(
              sources=["demo.pyx"],
              # library_dirs = ['/usr/lib/'],
              # runtime_library_dirs= ['/usr/lib/'],
              # include_dirs=[os.getcwd()],
              libraries=["libsleepy"],
              name = "hmidemo",
              language = 'c'
          )
]

setup(
  name = "Demos",
  ext_modules = cythonize(ext_modules)
)
