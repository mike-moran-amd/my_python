from distutils.core import setup
from __init__ import PARENT_PATH, VERSION, py_modules


setup(name=PARENT_PATH.name,
      version=VERSION,
      py_modules=py_modules(),
      )
